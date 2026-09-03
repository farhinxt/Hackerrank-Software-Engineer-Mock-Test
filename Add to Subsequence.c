#include <stdio.h>
#include <stdlib.h>

int compare(const void *a, const void *b) {
    int arg1 = *(const int *)a;
    int arg2 = *(const int *)b;
    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

int getMinOperations(int arr_count, int* arr) {
    if (arr_count <= 1) return 0;

    qsort(arr, arr_count, sizeof(int), compare);

    int max_freq = 1;
    int current_freq = 1;

    for (int i = 1; i < arr_count; i++) {
        if (arr[i] == arr[i-1]) {
            current_freq++;
        } else {
            if (current_freq > max_freq) {
                max_freq = current_freq;
            }
            current_freq = 1;
        }
    }
    if (current_freq > max_freq) {
        max_freq = current_freq;
    }

    int operations = 0;
    long long capacity = 1;
    while (capacity < max_freq) {
        capacity *= 2;
        operations++;
    }

    return operations;
}