#include "utils.h"

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

#define N 32 * MB

struct elem {
   struct elem *next;
};

int main() {
    srand ( time(NULL) );
    for (uint64_t s = 1; s < 512; s += 1) {
        uint64_t SIZE = s * KB;
        struct elem * array = malloc(SIZE);
        
        for (size_t i = 0; i < (SIZE - 1) / sizeof(struct elem); ++i) array[i].next = &array[i + 1];
        array[(SIZE - 1) / sizeof(struct elem)].next = array;

        // https://stackoverflow.com/a/13482822/13125945
        struct elem* pNext = NULL; 
        struct elem* pHead = NULL; 
        struct elem* pTail = NULL;
        int i = 0;
        // reset .next to NULL
        memset(array, 0, SIZE);
        pHead = &array[ rand() % (SIZE / sizeof(struct elem))];           
        pTail = pHead;
        for (i = 0; i < (SIZE - 1) / sizeof(struct elem); ++i)
        {   
            pTail->next = pTail;
            while ((pNext = &array[ rand() % (SIZE / sizeof(struct elem)) ]) && pNext->next);
            pTail->next = pNext;
            pTail = pNext;
        }
        pTail->next = pHead;

        //

        uint64_t start = rdtsc();
        int64_t dummy = 0;
        struct elem * current = pHead;
        for (size_t n = 0; n < N; ++n) {
            dummy += (int64_t)current;
            current = current->next;
        }
        uint64_t end = rdtsc();
        printf("(%ld,%ld),\n", SIZE / KB, (end - start));

        free(array);
    }
}