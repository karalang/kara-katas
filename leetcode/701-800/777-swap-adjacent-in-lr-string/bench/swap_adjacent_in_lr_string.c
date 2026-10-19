// Benchmark for #777: Swap Adjacent in LR String -- mirror of the ★ arm
// (two pointers), with the same workload as the Kāra program.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool can_transform(const char *s, const char *e, int64_t n) {
    int64_t i = 0, j = 0;
    for (;;) {
        while (i < n && s[i] == 'X') {
            i++;
        }
        while (j < n && e[j] == 'X') {
            j++;
        }
        if (i == n || j == n) {
            return i == n && j == n;
        }
        if (s[i] != e[j]) {
            return false;
        }
        if (s[i] == 'L' && i < j) {
            return false;
        }
        if (s[i] == 'R' && i > j) {
            return false;
        }
        i++;
        j++;
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, n = 10000;
    int64_t seed = 777;
    char *starts[64], *ends[64];
    for (int64_t g = 0; g < count; g++) {
        char *s = malloc(n + 1), *e = malloc(n + 1);
        for (int64_t i = 0; i < n; i++) {
            int64_t r = next_random(&seed) % 4;
            s[i] = r < 2 ? 'X' : r == 2 ? 'L' : 'R';
        }
        s[n] = 0;
        memcpy(e, s, n + 1);
        if (g % 4 < 2) {
            for (int m = 0; m < 100000; m++) {
                int64_t i = next_random(&seed) % (n - 1);
                if ((e[i] == 'X' && e[i + 1] == 'L') || (e[i] == 'R' && e[i + 1] == 'X')) {
                    char t = e[i];
                    e[i] = e[i + 1];
                    e[i + 1] = t;
                }
            }
        } else {
            int64_t k = g % 4 == 2 ? n - 2 : next_random(&seed) % (n - 1);
            while (!(e[k] == 'X' && e[k + 1] == 'R')) {
                k = k == 0 ? n - 2 : k - 1;
            }
            e[k] = 'R';
            e[k + 1] = 'X';
        }
        starts[g] = s;
        ends[g] = e;
    }
    int64_t yes = 0, checksum = 0;
    for (int64_t round = 0; round < 20000; round++) {
        int64_t g = (round * 7) % count;
        if (can_transform(starts[g], ends[g], n)) {
            yes++;
            checksum = (checksum * 31 + g + 1) % 1000000007;
        } else {
            checksum = (checksum * 31 + 7) % 1000000007;
        }
    }
    printf("20000 rounds of %lld letters: %lld reachable, checksum %lld\n", (long long)n, (long long)yes,
           (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        free(starts[g]);
        free(ends[g]);
    }
    return 0;
}
