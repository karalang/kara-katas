// LeetCode #2470: Number of Subarrays With LCM Equal to K -- the bench,
// the ★ arm in C: from each start the running LCM, the walk stopped once
// it no longer divides `k`, the gcd recursive as in Kāra.
#include <stdint.h>
#include <stdio.h>

static int64_t gcd(int64_t a, int64_t b) {
    return b == 0 ? a : gcd(b, a % b);
}

static int64_t subarray_lcm(const int64_t *nums, int64_t n, int64_t k) {
    int64_t count = 0;
    for (int64_t start = 0; start < n; start++) {
        int64_t lcm = 1;
        for (int64_t end = start; end < n; end++) {
            lcm = lcm / gcd(lcm, nums[end]) * nums[end];
            if (k % lcm != 0) break;
            if (lcm == k) count++;
        }
    }
    return count;
}

static int64_t seed = 2470;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 10 lists of 1000 numbers built once, each a random divisor of 720
    // but one in 50 any number from 1 to 1000; then 90 passes, each
    // setting one number of every list from the checksum so far, then
    // answering it with `k` 720 and folding the count plus the pass into
    // the checksum
    int64_t divisors[64], nd = 0;
    for (int64_t d = 1; d <= 720; d++)
        if (720 % d == 0) divisors[nd++] = d;
    static int64_t lists[10][1000];
    for (int a = 0; a < 10; a++) {
        for (int i = 0; i < 1000; i++) {
            if (next_random() % 50 == 0) {
                lists[a][i] = 1 + next_random() % 1000;
            } else {
                lists[a][i] = divisors[next_random() % nd];
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 90; p++) {
        for (int64_t a = 0; a < 10; a++) {
            lists[a][(check + a) % 1000] = divisors[check % nd];
            check = (check * 31 + subarray_lcm(lists[a], 1000, 720) + p) % 1000000007;
        }
    }
    printf("90 passes over 10 lists of 1000: checksum %lld\n", (long long)check);
    return 0;
}
