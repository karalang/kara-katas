// LeetCode #1534: Count Good Triplets -- bench: the ★ arm over 100 random
// arrays of 100 values up to 1000, each with its own a, b and c up to
// 1000, built once and answered 10 times. C mirror of triplets.kara.

#include <stdint.h>
#include <stdio.h>

static int64_t abs64(int64_t x) { return x < 0 ? -x : x; }

static int64_t count_good_triplets(const int64_t *arr, int n, int64_t a, int64_t b, int64_t c) {
    int64_t count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (abs64(arr[i] - arr[j]) > a) {
                continue;
            }
            for (int k = j + 1; k < n; k++) {
                if (abs64(arr[j] - arr[k]) <= b && abs64(arr[i] - arr[k]) <= c) {
                    count += 1;
                }
            }
        }
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1534;
    static int64_t arrs[100][100];
    int64_t as[100], bs[100], cs[100];
    for (int p = 0; p < 100; p++) {
        for (int i = 0; i < 100; i++) {
            arrs[p][i] = next_random(&seed) % 1001;
        }
        as[p] = next_random(&seed) % 1001;
        bs[p] = next_random(&seed) % 1001;
        cs[p] = next_random(&seed) % 1001;
    }
    int64_t check = 0;
    for (int pass = 0; pass < 10; pass++) {
        for (int p = 0; p < 100; p++) {
            check = mix(check, count_good_triplets(arrs[p], 100, as[p], bs[p], cs[p]));
        }
    }
    printf("10 passes over 100 arrays of 100 values: checksum %lld\n", (long long)check);
    return 0;
}
