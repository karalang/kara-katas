// LeetCode #1134: Armstrong Number -- the bench in C, the same algorithm
// and workload as is_armstrong.kara: every number from 1 to 15000000 asked
// in turn.
#include <stdint.h>
#include <stdio.h>

static int is_armstrong(int64_t n) {
    int64_t k = 0, m = n;
    while (m > 0) {
        k += 1;
        m /= 10;
    }
    int64_t total = 0;
    m = n;
    while (m > 0) {
        int64_t d = m % 10, p = 1;
        for (int64_t i = 0; i < k; i++) p *= d;
        total += p;
        m /= 10;
    }
    return total == n;
}

int main(void) {
    int64_t count = 0, sum = 0, check = 0;
    for (int64_t n = 1; n <= 15000000; n++) {
        if (is_armstrong(n)) {
            count += 1;
            sum += n;
            check = (check * 31 + n) % 1000000007;
        }
    }
    printf("1 to 15000000: %lld Armstrong numbers, summing to %lld, checksum %lld\n",
           (long long)count, (long long)sum, (long long)check);
    return 0;
}
