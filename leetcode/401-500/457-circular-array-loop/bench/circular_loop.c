// Benchmark for #457: mirror of circular_loop.kara (the ★ arm, slow and
// fast pointers) on the same workload.
#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_index(const int64_t *a, int64_t n, int64_t i) {
    return ((i + a[i]) % n + n) % n;
}

static bool circular_array_loop(const int64_t *nums, int64_t n) {
    int64_t *a = malloc(n * sizeof(int64_t));
    memcpy(a, nums, n * sizeof(int64_t));
    bool result = false;
    for (int64_t start = 0; start < n && !result; start++) {
        if (a[start] == 0) {
            continue;
        }
        bool forward = a[start] > 0;
        int64_t slow = start;
        int64_t fast = start;
        for (;;) {
            int64_t s = next_index(a, n, slow);
            int64_t f1 = next_index(a, n, fast);
            if (a[f1] == 0 || (a[f1] > 0) != forward) {
                break;
            }
            int64_t f2 = next_index(a, n, f1);
            if (a[f2] == 0 || (a[f2] > 0) != forward) {
                break;
            }
            slow = s;
            fast = f2;
            if (slow == fast) {
                if (next_index(a, n, slow) != slow) {
                    result = true;
                }
                break;
            }
        }
        if (result) {
            break;
        }
        // Nothing on this path reaches a valid cycle: clear it.
        int64_t i = start;
        while (a[i] != 0 && (a[i] > 0) == forward) {
            int64_t next = next_index(a, n, i);
            a[i] = 0;
            i = next;
        }
    }
    free(a);
    return result;
}

// ---- benchmark --------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t arrays = 10;
    const int64_t n = 1000000;
    const int64_t rounds = 5;
    int64_t seed = 457;
    int64_t *all[10];
    for (int64_t a = 0; a < arrays; a++) {
        all[a] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            int64_t step = 1 + next_random(&seed) % 1000;
            all[a][i] = next_random(&seed) % 2 == 0 ? step : -step;
        }
    }
    int64_t found = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t a = 0; a < arrays; a++) {
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            int64_t k = (hi * 65536 + lo) % (n - 1);
            int64_t one = all[a][k];
            int64_t two = all[a][k + 1];
            if (next_random(&seed) % 2 == 0) {
                all[a][k] = 1;
                all[a][k + 1] = n - 1;
            }
            bool has = circular_array_loop(all[a], n);
            all[a][k] = one;
            all[a][k + 1] = two;
            if (has) {
                found += 1;
            }
            checksum = (checksum * 31 + (has ? k + 1 : 0)) % 1000000007;
        }
    }
    printf("%" PRId64 " rounds on %" PRId64 " arrays of %" PRId64 ": %" PRId64 " with a loop, checksum %" PRId64 "\n",
           rounds, arrays, n, found, checksum);
    for (int64_t a = 0; a < arrays; a++) {
        free(all[a]);
    }
    return 0;
}
