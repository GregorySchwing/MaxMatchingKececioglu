#ifndef CSRGRAPH_CUH
#define CSRGRAPH_CUH

#include <thrust/host_vector.h>
#include <thrust/device_vector.h>
#include <thrust/execution_policy.h>
#include <thrust/reduce.h>
#include <thrust/for_each.h>
#include <thrust/transform.h>
#include <thrust/count.h>
#include <thrust/sort.h>

template <typename T>
__global__ void setNumInArray(T *arrays, T *index, T *value, int num_index);

struct CSRGraph {
public:
    CSRGraph(int _n, int _m, int * rows, int * cols);
    void createOffsets();

//private:
    const int INF = 1e9;
    unsigned int m;
    unsigned int n;
    thrust::device_vector<unsigned int> rows_d;
    thrust::device_vector<unsigned int> cols_d;
    thrust::device_vector<char> vals_d;
    thrust::host_vector<int> rows_h;
    thrust::host_vector<int> cols_h;
    thrust::host_vector<char> vals_h;
    thrust::host_vector<unsigned int> offsets_h;
    thrust::host_vector<unsigned int> keylabel_h;
    thrust::host_vector<unsigned int> nonzerodegrees_h;
    thrust::host_vector<unsigned int> degrees_h;
    thrust::device_vector<unsigned int> offsets_d;
    thrust::device_vector<unsigned int> keylabel_d;
    thrust::device_vector<unsigned int> nonzerodegrees_d;
    thrust::device_vector<unsigned int> degrees_d;
    thrust::host_vector<int> mate_h;
    thrust::device_vector<int> mate_d;
};

#endif
