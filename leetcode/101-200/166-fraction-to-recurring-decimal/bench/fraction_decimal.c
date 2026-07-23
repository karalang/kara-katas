#include <stdio.h>
#include <stdlib.h>

// The kata tracks seen remainders in a Map; C has no std map, so we hand-roll an
// epoch-stamped table: seen[rem] holds the pass id that last touched `rem`, so a
// per-pass "have I seen this remainder?" test is O(1) with no reset between
// passes (just bump `epoch`). Emits the identical digit sequence as the Map form.
static long frac_checksum(long num, long den, long *seen, long epoch) {
    long rem = num % den;
    long checksum = 0;
    if (rem == 0) return 0;
    long count = 0;
    while (rem != 0) {
        if (seen[rem] == epoch) {
            rem = 0; // cycle closed — stop
        } else {
            seen[rem] = epoch;
            rem *= 10;
            long digit = rem / den;
            checksum += digit;
            rem %= den;
            count++;
        }
    }
    (void)count;
    return checksum;
}

int main(void) {
    long passes = 500000;
    long denmax = 1025; // den <= 1024, so rem < 1024
    long *seen = calloc(denmax, sizeof(long));
    long state = 12345, sink = 0, epoch = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long num = state % 1000000;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long den = 2 + (state % 1023);
        epoch++;
        sink += frac_checksum(num, den, seen, epoch);
    }
    printf("%ld\n", sink);
    free(seen);
    return 0;
}
