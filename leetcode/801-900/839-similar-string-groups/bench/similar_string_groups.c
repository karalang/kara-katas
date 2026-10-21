// Benchmark for #839: Similar String Groups -- the ★ arm (union-find).
//
// Mirrors similar_string_groups.kara: every pair of words is compared
// once, stopping at a third difference, and a pair that differs in no
// position or in two joins its two groups, kept as a union-find forest
// with path halving. As in the Kāra program, each word is copied out to
// its own buffer for every count.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool similar(const unsigned char *a, const unsigned char *b, int64_t m) {
    int64_t diff = 0;
    for (int64_t k = 0; k < m; k++) {
        if (a[k] != b[k]) {
            diff += 1;
            if (diff > 2) return false;
        }
    }
    return diff != 1;
}

static int64_t find(int64_t *parent, int64_t x) {
    int64_t v = x;
    while (parent[v] != v) {
        parent[v] = parent[parent[v]];
        v = parent[v];
    }
    return v;
}

static int64_t num_similar_groups(char **strs, int64_t n, int64_t m) {
    unsigned char **words = malloc((size_t)n * sizeof *words);
    for (int64_t i = 0; i < n; i++) {
        words[i] = malloc((size_t)m);
        memcpy(words[i], strs[i], (size_t)m);
    }
    int64_t *parent = malloc((size_t)n * sizeof *parent);
    for (int64_t i = 0; i < n; i++) parent[i] = i;
    int64_t groups = n;
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = i + 1; j < n; j++) {
            int64_t a = find(parent, i);
            int64_t b = find(parent, j);
            if (a != b && similar(words[i], words[j], m)) {
                parent[a] = b;
                groups -= 1;
            }
        }
    }
    for (int64_t i = 0; i < n; i++) free(words[i]);
    free(words);
    free(parent);
    return groups;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 16 cases drawn once, each LeetCode's most and longest words, 300 of
    // 300 letters. The first word of case g is random; each later one is
    // an earlier word with one swap, or with three once in 1 + g % 4
    // words. Each round counts the groups of the next case.
    enum { COUNT = 16, N = 300, M = 300 };
    const int64_t rounds = 500;
    int64_t seed = 839;
    static char data[COUNT][N][M];
    static char *cases[COUNT][N];
    for (int64_t g = 0; g < COUNT; g++) {
        int64_t jump = 1 + g % 4;
        for (int64_t k = 0; k < M; k++) data[g][0][k] = (char)(97 + next_random(&seed) % 26);
        for (int64_t i = 1; i < N; i++) {
            int64_t from = next_random(&seed) % i;
            int64_t swaps = next_random(&seed) % jump == 0 ? 3 : 1;
            memcpy(data[g][i], data[g][from], M);
            for (int64_t s = 0; s < swaps; s++) {
                int64_t p = next_random(&seed) % M;
                int64_t q = next_random(&seed) % M;
                char t = data[g][i][p];
                data[g][i][p] = data[g][i][q];
                data[g][i][q] = t;
            }
        }
        for (int64_t i = 0; i < N; i++) cases[g][i] = data[g][i];
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t groups = num_similar_groups(cases[round % COUNT], N, M);
        total += groups;
        checksum = (checksum * 31 + groups + round) % 1000000007;
    }
    printf("%lld rounds of %d cases: %lld groups, checksum %lld\n", (long long)rounds, COUNT, (long long)total,
           (long long)checksum);
    return 0;
}
