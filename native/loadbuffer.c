// SRC: Compressed version of https://github.com/travisdowns/robsize
#include "utils.h"

#include <assert.h>
#include <getopt.h>
#include <malloc.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

#define ADD_BYTE(val) do{ibuf[pbuf] = (val); pbuf++;} while(0)
#define ADD_WORD(val) do{*(unsigned short*)(&ibuf[pbuf]) = (val); pbuf+=2;} while(0)
#define ADD_DWORD(val) do{*(unsigned int*)(&ibuf[pbuf]) = (val); pbuf+=4;} while(0)

//config
static int start_icount = 40;
static int stop_icount = 80;

static int its = 8192; // iterations
const int MAX_ICOUNT = 400; // max payload size
const int memsize = 268435456;
static int outer_its = 64;

const int operation = 1; // 0 load, 1 store

int add_filler(unsigned char* ibuf)
{
    int pbuf = 0;
    switch (operation) {
        case 0:  ADD_BYTE(0x8b); ADD_BYTE(0x1c); ADD_BYTE(0x24); break;  // mov    ebx, [rsp]
        case 1:  ADD_BYTE(0x89); ADD_BYTE(0x5c); ADD_BYTE(0x24); ADD_BYTE(0xf8); break; // mov [rsp-0x8], ebx
    }

    return pbuf;
}

/**
 * icount - the number of instructions between loads
 */
void make_routine(unsigned char* ibuf, void *p1, void *p2, const int icount)
{

    int pbuf = 0;

    ADD_BYTE(0x53);		// push ebx
    ADD_BYTE(0x55);		// push ebp
    ADD_BYTE(0x56);		// push esi
    ADD_BYTE(0x57);		// push edi

    ADD_WORD(0xb948);		// mov rcx, p1;
    ADD_DWORD((unsigned long long)p1);
    ADD_DWORD((unsigned long long)p1>>32LL);

    ADD_WORD(0xba48);		// mov rdx, p2;
    ADD_DWORD((unsigned long long)p2);
    ADD_DWORD((unsigned long long)p2>>32LL);

    ADD_WORD(0xb848);		// mov rax, its;
    ADD_DWORD(its);
    ADD_DWORD(0);

    int loop_start = pbuf;		// loop branch target.

    ADD_WORD(0x8b48);	// mov r64, r/m64
    ADD_BYTE(0x09);		//	... rcx, [rcx]

    for (int j = 0; j < icount; j++)
        pbuf += add_filler(ibuf+pbuf);

    ADD_WORD(0x8b48);	// mov r64, r/m64
    ADD_BYTE(0x12);	//		... edx, [edx]

    for (int j=0; j < icount; j++)
        pbuf += add_filler(ibuf+pbuf);

    ADD_WORD(0xe883); // sub eax
    ADD_BYTE(0x1);		//    1
    ADD_WORD(0x850f); // jne loop_start
    ADD_DWORD(loop_start - pbuf - 4);

    ADD_BYTE(0x5f);		// pop edi
    ADD_BYTE(0x5e);		// pop esi
    ADD_BYTE(0x5d);		// pop ebp
    ADD_BYTE(0x5b);		// pop ebx

    ADD_BYTE(0xc3);	// c3 ret

    mprotect(ibuf, pbuf, PROT_READ|PROT_WRITE|PROT_EXEC);
}

static inline unsigned long long my_rand (unsigned long long limit)
{
    return ((unsigned long long)(((unsigned long long)rand()<<48)^((unsigned long long)rand()<<32)^((unsigned long long)rand()<<16)^(unsigned long long)rand())) % limit;
}

void init_dbuf(void ** dbuf, int size, int cycle_length)
{
    for (int i=0;i<size;i++)
        dbuf[i] = &dbuf[i];
    for (int i=size-1;i>0;i--)
    {
        if (i & 0x1ff) continue;
        if (i < cycle_length) continue;
        unsigned int k = my_rand(i/cycle_length) * cycle_length + (i%cycle_length);
        void* temp = dbuf[i];
        dbuf[i] = dbuf[k];
        dbuf[k] = temp;
    }
}

int main() {

    unsigned char *ibuf = (unsigned char*)valloc(1048576);
    void ** dbuf = (void**)valloc(memsize);

    init_dbuf(dbuf, memsize/sizeof(void*), 8192/sizeof(void*));
    void(*routine)() = (void(*)())ibuf;
    
    const char *delim = "\t";
    printf("%s%s%s%s%s%s%s\n", "ICOUNT", delim, "MIN", delim, "AVG", delim, "MAX");

    for (int icount = start_icount; icount <= stop_icount; icount += 1)
    {
        make_routine(ibuf, dbuf, dbuf+((8388608+4096)/sizeof(void*)), icount);
        routine();

        long long min_diff = 0x7fffffffffffffffLL;
        long long max_diff = 0x0;
        long long sum_diff = 0;
        for (int i=0;i<outer_its;i++) {

            long long start = rdtsc();
            routine();
            long long stop = rdtsc();

            sum_diff += (stop - start);
            if (min_diff > (stop - start))
            {
                min_diff = stop-start;
            }
            if (max_diff < (stop - start))
            {
                max_diff = stop-start;
            }
        }
        printf("%d%s%.2f%s%.2f%s%.2f\n", icount, delim, 0.5*min_diff/its, delim, 0.5*sum_diff/its/outer_its,
                delim, 0.5*max_diff/its);
    }

    free (dbuf);
    free (ibuf);

}