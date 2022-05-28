#ifndef NATIVE_UTILS_H
#define NATIVE_UTILS_H

#include <stdint.h>

#define KB 1024
#define MB 1024 * 1024

// src: https://github.com/IAIK/flush_flush/blob/master/sc/cacheutils.h
uint64_t rdtsc() {
  uint64_t a, d;
  asm volatile ("mfence");
  asm volatile ("rdtsc" : "=a" (a), "=d" (d));
  a = (d<<32) | a;
  asm volatile ("mfence");
  return a;
}

// src: https://github.com/IAIK/flush_flush/blob/master/sc/cacheutils.h
void maccess(void* p)
{
  asm volatile ("mov (%0), %%eax\n"
    :
    : "c" (p)
    : "eax");
}

// src: https://github.com/IAIK/flush_flush/blob/master/sc/cacheutils.h
void flush(void* p) {
    asm volatile ("clflush 0(%0)\n"
      :
      : "c" (p)
      : "rax");
}

uint64_t probe(void* p) {
  uint64_t start = rdtsc();
  maccess(p);
  return rdtsc() - start;
}

#endif