// LeetCode #1227 bench: the running-sum arm in C, over the same 1000
// random n up to 10^5 as the Kāra bench.
#include <stdio.h>

static double nth_person_gets_nth_seat(long n) {
    double f = 1.0, sum = 0.0;
    for (long m = 2; m <= n; m++) {
        f = (1.0 + sum) / (double)m;
        sum += f;
    }
    return f;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    long seed = 1227;
    double total = 0.0;
    for (int i = 0; i < 1000; i++) {
        long a = next_random(&seed) % 30000 * 3;
        long n = a + next_random(&seed) % 10000 + 1;
        total += nth_person_gets_nth_seat(n);
    }
    printf("1000 random n up to 10^5: total %.5f\n", total);
    return 0;
}
