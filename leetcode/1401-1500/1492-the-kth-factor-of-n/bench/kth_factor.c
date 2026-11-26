// LeetCode #1492: The kth Factor of n -- the bench in C, mirroring
// kth_factor.kara: every i from 1 to n tried in order.
#include <stdint.h>
#include <stdio.h>

static int32_t kth_factor(int32_t n, int32_t k) {
    int32_t left = k;
    for (int32_t i = 1; i <= n; i++) {
        if (n % i == 0) {
            left--;
            if (left == 0) return i;
        }
    }
    return -1;
}

int main(void) {
    int64_t check = 0;
    for (int64_t pass = 0; pass < 400; pass++) {
        for (int64_t n = 1; n <= 1000; n++) {
            int32_t k = (int32_t)(1 + (n + pass + check) % 40);
            check = (check * 31 + kth_factor((int32_t)n, k) + 2) % 1000000007;
        }
    }
    printf("400 passes over n up to 1000: checksum %lld\n", (long long)check);
    return 0;
}
