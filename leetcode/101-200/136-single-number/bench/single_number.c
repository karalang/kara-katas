#include <stdio.h>
#include <stdlib.h>

/* Single-number (XOR-fold) as a wide reduction kernel.
 *
 * Build-once + punch: one big array is generated once with the canonical
 * single-number shape — M value pairs plus one lone element — using a
 * deterministic 32-bit LCG (overflow-safe in i64; values from the HIGH bits to
 * dodge the LCG's short-period low bits). Each pass toggles one bit of one
 * element (so the array — and its fold — changes every pass and the optimizer
 * cannot hoist) then XOR-folds the whole array: the paired values cancel and
 * the lone survivor drops out. Per-op is one XOR, so total work is made large
 * with a wide array and many passes. Sink = running total of the folds. */

static long single_number(const long *nums, long n) {
    long acc = 0;
    for (long i = 0; i < n; i++) acc ^= nums[i];
    return acc;
}

int main(void) {
    long pairs = 140000, passes = 3400;
    long n = 2 * pairs + 1;
    long *nums = malloc(n * sizeof(long));
    long state = 12345, w = 0;
    for (long k = 0; k < pairs; k++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long v = state >> 16;
        nums[w++] = v;
        nums[w++] = v;
    }
    state = (state * 1103515245L + 12345L) & 2147483647L;
    nums[w++] = state >> 16;  /* the lone element */

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = (p * 97 + 13) % n;
        nums[idx] = nums[idx] ^ (1L << (p % 14));  /* punch: toggle a low bit */
        sink += single_number(nums, n);
    }
    printf("%ld\n", sink);
    free(nums);
    return 0;
}
