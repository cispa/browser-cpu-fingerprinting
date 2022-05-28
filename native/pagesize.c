#include "utils.h"

#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>

#define MAX_SIZE 256 * KB
#define STEPS 8192

// 4 KB, 8 KB, 64 KB, 256 KB, 1 MB, 2 MB, 4 MB, 16 MB, 256 MB

int main() {
    uint32_t * buffer = malloc(sizeof(uint64_t) * MAX_SIZE);

    for (uint64_t i = 0; i <= STEPS; i += 8) {

        uint64_t start = rdtsc();
        uint32_t tmp = buffer[i];
        uint64_t end = rdtsc();
        printf("(%ld,%ld),\n", i, end - start);

    }

    free(buffer);
}