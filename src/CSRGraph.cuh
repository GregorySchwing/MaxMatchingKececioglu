#ifndef CSRGRAPH
#define CSRGRAPH
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>
#include <thrust/execution_policy.h>
#include <thrust/reduce.h>
#include <thrust/for_each.h>
#include <thrust/transform.h>
#include <thrust/count.h>
#include <thrust/sort.h>


// kernel function
template <typename T>
__global__ void setNumInArray(T *arrays, T *index, T *value, int num_index)
{
  int tid = threadIdx.x + blockDim.x * blockIdx.x;
  if (tid >= num_index || index[tid] < tid)
    return;
  arrays[index[tid]] = value[tid];
}

struct CSRGraph
{
  const int INF = 1e9;

  CSRGraph(int _n, int _m)
  {

    m = _m;
    n = _n;
    offsets_h.resize(n + 1);
    degrees_h.resize(n);

    rows_h.resize(2 * m);
    cols_h.resize(2 * m);
    vals_h.resize(2 * m, 1);

    rows_d.resize(2 * m);
    // This will be the dst ptr array.
    cols_d.resize(2 * m);
    vals_d.resize(2 * m, 1);

    offsets_d.resize(n + 1);

    keylabel_d.resize(n);
    nonzerodegrees_d.resize(n);
    // This will be the degrees array.
    degrees_d.resize(n);


  }

  void createOffsets()
  {
    rows_d = rows_h;
    cols_d = cols_h;
    thrust::sort_by_key(thrust::device, rows_d.begin(), rows_d.end(), cols_d.begin());
    thrust::pair<thrust::device_vector<unsigned int>::iterator, thrust::device_vector<unsigned int>::iterator> new_end;
    new_end = thrust::reduce_by_key(thrust::device, rows_d.begin(), rows_d.end(), vals_d.begin(), keylabel_d.begin(), nonzerodegrees_d.begin());
    int block_size = 64;
    int num_blocks = (n + block_size - 1) / block_size;
    unsigned int *degrees_ptr_d = thrust::raw_pointer_cast(degrees_d.data());
    unsigned int *keylabel_ptr_d = thrust::raw_pointer_cast(keylabel_d.data());
    unsigned int *nonzerodegrees_ptr_d = thrust::raw_pointer_cast(nonzerodegrees_d.data());
    setNumInArray<unsigned int><<<num_blocks, block_size>>>(degrees_ptr_d, keylabel_ptr_d, nonzerodegrees_ptr_d, n);
    thrust::inclusive_scan(thrust::device, degrees_d.begin(), degrees_d.end(), offsets_d.begin() + 1); // in-place scan
    offsets_h = offsets_d;
    degrees_h = degrees_d;
    rows_h = rows_d;
    cols_h = cols_d;

    keylabel_d.clear();
    vals_d.clear();
    nonzerodegrees_d.clear();
  }

  unsigned int m; // Number of Edges
  unsigned int n; // Number of Vertices

  thrust::device_vector<unsigned int> rows_d;
  thrust::device_vector<unsigned int> cols_d;
  thrust::device_vector<char> vals_d;


  thrust::host_vector<unsigned int> rows_h;
  thrust::host_vector<unsigned int> cols_h;
  thrust::host_vector<char> vals_h;

  thrust::host_vector<unsigned int> offsets_h;
  thrust::host_vector<unsigned int> keylabel_h;
  thrust::host_vector<unsigned int> nonzerodegrees_h;
  thrust::host_vector<unsigned int> degrees_h;

  thrust::device_vector<unsigned int> offsets_d;
  thrust::device_vector<unsigned int> keylabel_d;
  thrust::device_vector<unsigned int> nonzerodegrees_d;
  thrust::device_vector<unsigned int> degrees_d;

  thrust::host_vector<int> mate_h; // n
  thrust::device_vector<int> mate_d; // n

};

#endif