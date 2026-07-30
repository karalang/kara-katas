/* Equal-safety C twin of summary_ranges.c — a PROBE, not a benchmark mirror.
 *
 * Not wired into bench.sh and not part of the cross-language parity set. It
 * exists to isolate one question: how much of this kata's apparent Kara deficit
 * (4.19x vs `rust -O`, 4.73x vs `clang -O3`) is the overflow-check semantics
 * rather than karac's codegen?
 *
 * Every add in the scan goes through __builtin_add_overflow with a trap on
 * overflow, which is what Kara does by default and what `rustc -C
 * overflow-checks=on` does. Build both arms and compare (2026-07-30, x86):
 *
 *   clang -O3 -march=x86-64-v3 -DCHK=1 summary_ranges_ovf.c   ->  1124 ms
 *   clang -O3 -march=x86-64-v3 -DCHK=0 summary_ranges_ovf.c   ->   245 ms
 *   karac build summary_ranges.kara                           ->  1107 ms
 *
 * So the checks cost clang 4.6x, they cost `rustc` 4.8x (268.8 -> 1293 ms), and
 * Kara's checked lowering is FASTER than either. The deficit is the guarantee,
 * not the compiler. Reducing it means eliding provably-safe checks, not
 * emitting them better. See ../../../BENCHMARKS.md for the write-up.
 *
 * Sink must match summary_ranges.kara exactly: 333678318888000.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define CHK 1
#if CHK
#define ADD(a,b,out) do{ if(__builtin_add_overflow((a),(b),(out))) { fprintf(stderr,"overflow\n"); exit(1);} }while(0)
#else
#define ADD(a,b,out) do{ *(out)=(a)+(b); }while(0)
#endif
static int64_t summary_metric(const int64_t *nums, int64_t n){
    int64_t i=1, start=nums[0], ranges=0, esum=0, t;
    while(i<=n){
        int64_t prev1; ADD(nums[i-1],(int64_t)1,&prev1);
        if(i==n || nums[i]!=prev1){
            int64_t end=nums[i-1];
            ADD(ranges,(int64_t)1,&ranges);
            ADD(esum,start,&t); ADD(t,end,&esum);
            if(i<n) start=nums[i];
        }
        ADD(i,(int64_t)1,&i);
    }
    ADD(ranges,esum,&t); return t;
}
int main(void){
    int64_t n=1000000, passes=250;
    int64_t *nums=malloc(sizeof(int64_t)*(size_t)n);
    int64_t state=12345, v=0;
    for(int64_t c=0;c<n;c++){ state=(state*1103515245+12345)&2147483647; v=v+1+(state%3); nums[c]=v; }
    int64_t sink=0;
    for(int64_t p=0;p<passes;p++) sink+=summary_metric(nums,n);
    printf("%lld\n",(long long)sink); free(nums); return 0;
}
