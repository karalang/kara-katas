#include <stdio.h>
#include <stdlib.h>

static long window_majority_sum(const long *nums, long s, long win) {
    long cand1 = 0, cand2 = 0, count1 = 0, count2 = 0;
    long end = s + win;
    for (long k = s; k < end; k++) {
        long x = nums[k];
        if (count1 > 0 && x == cand1) {
            count1 += 1;
        } else if (count2 > 0 && x == cand2) {
            count2 += 1;
        } else if (count1 == 0) {
            cand1 = x;
            count1 = 1;
        } else if (count2 == 0) {
            cand2 = x;
            count2 = 1;
        } else {
            count1 -= 1;
            count2 -= 1;
        }
    }

    long real1 = 0, real2 = 0;
    for (long j = s; j < end; j++) {
        long x = nums[j];
        if (count1 > 0 && x == cand1) {
            real1 += 1;
        } else if (count2 > 0 && x == cand2) {
            real2 += 1;
        }
    }

    long threshold = win / 3;
    long total = 0;
    if (count1 > 0 && real1 > threshold) total += cand1;
    if (count2 > 0 && real2 > threshold) total += cand2;
    return total;
}

int main(void) {
    long n = 3000000;
    long win = 16;

    long *nums = malloc(n * sizeof(long));
    long state = 12345;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        nums[c] = (state % 3) + 1;
    }

    long sink = 0;
    long last = n - win;
    for (long s = 0; s <= last; s++) {
        sink += window_majority_sum(nums, s, win);
    }
    printf("%ld\n", sink);
    free(nums);
    return 0;
}
