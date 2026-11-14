// LeetCode #1531: String Compression II -- bench: the ★ arm over 300
// random strings of 1 to 100 letters, each over its own 1 to 4 letters with
// k from 0 to its length, built once and answered 10 times. The table is a
// fresh `malloc` per answer, as the other languages allocate one.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t run_length(int64_t count) {
    if (count == 1) return 1;
    if (count < 10) return 2;
    if (count < 100) return 3;
    return 4;
}

static int64_t get_length_of_optimal_compression(const char *b, int64_t n, int64_t k) {
    int64_t w = k + 1;
    int64_t *best = calloc((size_t)((n + 1) * w), sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) {
        for (int64_t j = 0; j <= k; j++) {
            int64_t shortest = n + 1;
            if (j > 0) {
                shortest = best[(i + 1) * w + j - 1];
            }
            int64_t same = 0, other = 0;
            for (int64_t end = i; end < n; end++) {
                if (b[end] == b[i]) {
                    same++;
                } else {
                    other++;
                }
                if (other > j) {
                    break;
                }
                int64_t cand = run_length(same) + best[(end + 1) * w + j - other];
                if (cand < shortest) {
                    shortest = cand;
                }
            }
            best[i * w + j] = shortest;
        }
    }
    int64_t answer = best[k];
    free(best);
    return answer;
}

static int64_t seed = 1531;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

int main(void) {
    enum { COUNT = 300 };
    static char *strs[COUNT];
    static int64_t lens[COUNT];
    static int64_t ks[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t n = next_random() % 100 + 1;
        int64_t over = next_random() % 4 + 1;
        strs[c] = malloc((size_t)n + 1);
        for (int64_t i = 0; i < n; i++) {
            strs[c][i] = (char)(97 + next_random() % over);
        }
        strs[c][n] = 0;
        lens[c] = n;
        ks[c] = next_random() % (n + 1);
    }
    int64_t check = 0;
    for (int pass = 0; pass < 10; pass++) {
        for (int c = 0; c < COUNT; c++) {
            check = mix(check, get_length_of_optimal_compression(strs[c], lens[c], ks[c]));
        }
    }
    printf("10 passes over 300 strings of up to 100 letters: checksum %lld\n", (long long)check);
    for (int c = 0; c < COUNT; c++) {
        free(strs[c]);
    }
    return 0;
}
