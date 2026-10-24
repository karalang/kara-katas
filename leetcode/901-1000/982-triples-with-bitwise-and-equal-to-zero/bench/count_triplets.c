// Benchmark: LeetCode #982 Triples with Bitwise AND Equal To Zero -- the
// ★ arm, pair counts and the free bits' submasks, on lists of LeetCode's
// largest size. Mirrors count_triplets.kara, .rs, .py and go-seq/.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t count_triplets(const int64_t *nums, int n) {
    int64_t all = 0;
    for (int i = 0; i < n; i++) {
        all |= nums[i];
    }
    int64_t size = 1;
    while (size <= all) {
        size *= 2;
    }
    int64_t full = size - 1;
    int64_t *pairs = calloc((size_t)size, sizeof(int64_t));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            pairs[nums[i] & nums[j]] += 1;
        }
    }
    int64_t triples = 0;
    for (int i = 0; i < n; i++) {
        int64_t free_bits = full ^ nums[i];
        int64_t s = free_bits;
        for (;;) {
            triples += pairs[s];
            if (s == 0) {
                break;
            }
            s = (s - 1) & free_bits;
        }
    }
    free(pairs);
    return triples;
}

static int64_t seed = 982;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 15;
    static int64_t lists[20][1000];
    for (int l = 0; l < 20; l++) {
        for (int i = 0; i < 1000; i++) {
            lists[l][i] = next_random() % 65536;
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int64_t t = count_triplets(lists[(r + i) % 20], 1000);
            total += t;
            check = (check * 31 + t) % 1000000007;
        }
    }
    printf("%d rounds over 20 lists of 1000 values: triples %lld, checksum %lld\n", rounds, (long long)total,
           (long long)check);
    return 0;
}
