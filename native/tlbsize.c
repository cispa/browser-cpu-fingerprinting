#include "utils.h"

#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>

#define MAX_SIZE KB * MB
#define STEPS 256
#define PAGES 256
#define PAGESIZE 4096
#define LARGESTEPS 256 * MB

// 4 KB, 8 KB, 64 KB, 256 KB, 1 MB, 2 MB, 4 MB, 16 MB, 256 MB

static inline uint32_t mlog2(const uint32_t x) {
  uint32_t y;
  asm ( "\tbsr %1, %0\n"
      : "=r"(y)
      : "r" (x)
  );
  return y;
}

void shuffle(int *array, size_t n)
{
    if (n > 1) 
    {
        size_t i;
        for (i = 0; i < n - 1; i++) 
        {
          size_t j = i + rand() / (RAND_MAX / (n - i) + 1);
          int t = array[j];
          array[j] = array[i];
          array[i] = t;
        }
    }
}

int main() {
    uint8_t * buffer = malloc(sizeof(uint8_t) * MAX_SIZE);
    int * indices = malloc(sizeof(int) * 1);

    for (uint32_t page = 1; page <= PAGES; page++) {

        indices = realloc(indices, sizeof(int) * page);

        for (uint32_t j = 0; j < page; j++) {
            indices[j] = j * PAGESIZE;
        }

        //shuffle(indices, page);

        // put in tlb
        for (uint32_t j = 0; j < page; j++) {
            buffer[indices[j]] = j;
        }

        // uint64_t minimum = INT64_MAX;
        // for (uint64_t step = 0; step < STEPS; step++) {
        //     uint64_t maximum = 0;
        //     for (uint32_t j = 0; j < page; j++) {
        //         flush(&buffer[indices[j]]);
        //         uint64_t start = rdtsc();
        //         maccess(buffer + indices[j]);
        //         uint64_t time = rdtsc() - start;
        //         if (time > maximum) maximum = time;
        //     }
        //     if (minimum > maximum) minimum = maximum;
        // }

        // printf("(%d,%ld),\n", page, minimum);

        uint64_t start = rdtsc();

        for (uint64_t step = 0; step < LARGESTEPS; step++) {
            maccess(buffer + indices[step % page]);
        }

        uint64_t time = rdtsc() - start;

        printf("(%d,%ld),\n", page, time);

    }

    free(indices);
    free(buffer);
}