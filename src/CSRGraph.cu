#include "CSRGraph.cuh"

// kernel function
template <typename T>
__global__ void setNumInArray(T *arrays, T *index, T *value, int num_index)
{
  int tid = threadIdx.x + blockDim.x * blockIdx.x;
  if (tid >= num_index || index[tid] < tid)
    return;
  arrays[index[tid]] = value[tid];
}

CSRGraph::CSRGraph(int _n, int _m, int * rows, int * cols) 
{

  m = _m;
  n = _n;
  offsets_h.resize(n + 1);
  degrees_h.resize(n);

  //rows_h.resize(2 * m);
  //cols_h.resize(2 * m);
  rows_h.assign(rows, rows + 2*m);
  cols_h.assign(cols, cols + 2*m);
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

  mate_h.resize(n,-1);
  mate_d.resize(n,-1);

  createOffsets();
}

void CSRGraph::createOffsets()
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