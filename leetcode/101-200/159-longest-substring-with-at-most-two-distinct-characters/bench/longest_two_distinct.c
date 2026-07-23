#include <stdio.h>
#include <stdlib.h>

// The kata tracks the window's distinct chars with a Map[char,i64]; C has no
// map, so we hand-roll the identical structure as a flat ALPHABET-sized count
// table (alphabet is only 8), which is exactly what the other mirrors use.
static long longest(const long *buf, long lo, long hi, long alphabet) {
    long counts[8];
    for (long a = 0; a < alphabet; a++) counts[a] = 0;
    long distinct = 0;
    long left = lo;
    long best = 0;
    for (long right = lo; right < hi; right++) {
        long c = buf[right];
        if (counts[c] == 0) distinct++;
        counts[c]++;
        while (distinct > 2) {
            long lc = buf[left];
            counts[lc]--;
            if (counts[lc] == 0) distinct--;
            left++;
        }
        long w = right - left + 1;
        if (w > best) best = w;
    }
    return best;
}

int main(void) {
    long size = 20000;
    long alphabet = 8;
    long width = 96;
    long reps = 100;

    long *buf = malloc((size_t)size * sizeof(long));
    long state = 12345;
    for (long c = 0; c < size; c++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        buf[c] = state % alphabet;
    }


    long ranges = size - width;
    long sink = 0;
    for (long rep = 0; rep < reps; rep++) {
        long idx = (rep * 131 + 7) % size;
        buf[idx] = (buf[idx] + 1) % alphabet;
        for (long start = 0; start < ranges; start++) {
            sink += longest(buf, start, start + width, alphabet);
        }
    }
    printf("%ld\n", sink);
    return 0;
}
