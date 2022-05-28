#include <stdio.h> 
#include <stdlib.h>
#include <time.h>

#include "utils.h"

#define KB 1024
#define MB 1024 * 1024

int main() {
    unsigned int steps = 256 * 1024 * 1024;
    static int arr[24 * MB];
    unsigned long long lengthMod;
    unsigned int i;
    double timeTaken;
    clock_t start;
    unsigned long long sizes[] = { 
        1 * KB, 4 * KB, 8 * KB, 16 * KB, 32 * KB, 64 * KB, 128 * KB, 256 * KB,
        512 * KB, 1 * MB, 2 * MB, 4 * MB, 6 * MB, 8 * MB, 10 * MB, 12 * MB,
        14 * MB, 16 * MB, 18 * MB, 20 * MB, 22 * MB, 24 * MB
    };
    int s;

    // for each size to test for ... 
    for (s = 0; s < sizeof(sizes)/sizeof(unsigned long long); s++) {
        int lengthMod = sizes[s] - 1;
        uint64_t start = rdtsc();
        for (int i = 0; i < steps; i++) {
            arr[(i * 16) & lengthMod]++;
        }
        uint64_t end = rdtsc();
        printf("(%lld,%ld),", sizes[s] / KB, end - start);
    }

    return 0;
}
