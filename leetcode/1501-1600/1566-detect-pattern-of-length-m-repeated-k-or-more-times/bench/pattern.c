// LeetCode #1566: Detect Pattern of Length M Repeated K or More Times --
// bench: the ★ arm (a run of agreements m apart) over 20 arrays of 100000
// values of 1 to 100, built once, half with a pattern planted near the
// end, each asked for m from 1 to 50 with k of 3.
// C mirror of pattern.kara.

#include <stdint.h>
#include <stdio.h>

#define N 100000

static int contains_pattern(const int64_t *arr, int64_t n, int64_t m, int64_t k) {
    int64_t run = 0;
    for (int64_t i = 0; i < n - m; i++) {
        if (arr[i] == arr[i + m]) {
            run++;
            if (run == m * (k - 1)) return 1;
        } else {
            run = 0;
        }
    }
    return 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1566;
    static int64_t arrays[20][N];
    for (int64_t a = 0; a < 20; a++) {
        for (int64_t i = 0; i < N; i++) arrays[a][i] = next_random(&seed) % 100 + 1;
        if (a % 2 == 1) {
            int64_t m = 1 + a % 50;
            int64_t start = N - 3 * m - next_random(&seed) % 100;
            for (int64_t i = m; i < 3 * m; i++) arrays[a][start + i] = arrays[a][start + i % m];
        }
    }
    int64_t check = 0, found = 0;
    for (int64_t m = 1; m <= 50; m++)
        for (int64_t a = 0; a < 20; a++) {
            int yes = contains_pattern(arrays[a], N, m, 3);
            if (yes) found++;
            check = mix(check, yes ? m * 100 + a : 0);
        }
    printf("m from 1 to 50 over 20 arrays of 100000 values: %lld with a pattern, checksum %lld\n", (long long)found,
           (long long)check);
    return 0;
}
