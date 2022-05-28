#include "utils.h"

#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>

#define MAX_SIZE KB * MB
#define STEPS 20 * MB
#define PAGESIZE 4096
#define ENTRIES MB
#define FENCE 200


void shuffle(int *array, size_t n) {
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
    uint64_t randomStuff = 0;
    uint8_t * buffer = malloc(sizeof(uint8_t) * MAX_SIZE);
    uint8_t * buffer2 = malloc(sizeof(uint8_t) * MAX_SIZE);
    int * indices = malloc(sizeof(int) * ENTRIES);

    for (uint32_t j = 0; j < ENTRIES; j++) {
        indices[j] = j * 256;
    }

    shuffle(indices, ENTRIES);

    //touch
    for (uint32_t j = 0; j < ENTRIES; j++) {
        uint32_t index = j * 256 + 128;
        buffer[index] = j;
        buffer2[index] = j + 1;
    }

    uint64_t time = 0;
    uint64_t start;

    for (uint64_t step = 0; step < ENTRIES; step++) {
        // flush(buffer + indices[ step ]);
        // flush(buffer + indices[ step ] + 64);
        // for (uint64_t i = 0; i < FENCE; i++) {
        //     randomStuff += 1;
        // }
        maccess(buffer + indices[ step ]);
        start = rdtsc();
        maccess(buffer + indices[ step ] + 64);
        time += rdtsc() - start;
    }
    
    printf("Time A - %ld\n", time);

    time = 0;

    for (uint64_t step = 0; step < ENTRIES; step++) {
        // flush(buffer2 + indices[ step ]);
        // flush(buffer2 + indices[ step ] + 16);
        // for (uint64_t i = 0; i < FENCE; i++) {
        //     randomStuff += 1;
        // }
        maccess(buffer2 + indices[ step ]);
        start = rdtsc();
        maccess(buffer2 + indices[ step ] + 16);
        time += rdtsc() - start;
    }
    
    printf("Time B - %ld\n", time);

    free(indices);
    free(buffer);
    free(buffer2);

}