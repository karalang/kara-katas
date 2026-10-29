// LeetCode #1015: Smallest Integer Divisible by K -- bench
// Mirrors repunit.kara; see ../README.md § Benchmarks.
#include <stdint.h>
#include <stdio.h>

static int64_t smallest_repunit_div_by_k(int64_t k) {
    if (k % 2 == 0 || k % 5 == 0) {
        return -1;
    }
    int64_t r = 0;
    for (int64_t length = 1; length < k + 1; length++) {
        r = (r * 10 + 1) % k;
        if (r == 0) {
            return length;
        }
    }
    return -1;
}

int main(void) {
    int64_t last = 30000;
    int64_t none = 0;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t k = 1; k < last + 1; k++) {
        int64_t answer = smallest_repunit_div_by_k(k);
        if (answer < 0) {
            none++;
        } else {
            total += answer;
        }
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("k = 1..%lld: %lld with no answer, the rest sum to %lld, checksum %lld\n", (long long)last,
           (long long)none, (long long)total, (long long)check);
    return 0;
}
