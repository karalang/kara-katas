// Benchmark: LeetCode #969 Pancake Sorting -- the ★ arm, the largest
// pancake to the bottom one at a time, on 200 random stacks of 100
// pancakes. Mirrors pancake_sort.kara, .rs, .py and go-seq/. Each call
// mallocs its copy of the stack and its flips, as the other languages
// allocate theirs.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void flip(int64_t *a, int64_t k) {
    int64_t i = 0, j = k - 1;
    while (i < j) {
        int64_t t = a[i];
        a[i] = a[j];
        a[j] = t;
        i++;
        j--;
    }
}

// The flips in *out, their count returned; at most 2(n - 1).
static int64_t pancake_sort(const int64_t *arr, int64_t n, int64_t **out) {
    int64_t *a = malloc(sizeof(int64_t) * n);
    memcpy(a, arr, sizeof(int64_t) * n);
    int64_t *flips = malloc(sizeof(int64_t) * (2 * n + 1));
    int64_t len = 0;
    for (int64_t size = n; size > 1; size--) {
        int64_t i = 0;
        while (a[i] != size) i++;
        if (i != size - 1) {
            if (i != 0) {
                flip(a, i + 1);
                flips[len++] = i + 1;
            }
            flip(a, size);
            flips[len++] = size;
        }
    }
    free(a);
    *out = flips;
    return len;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void random_permutation(int64_t *a, int64_t n, int64_t *seed) {
    for (int64_t v = 1; v <= n; v++) a[v - 1] = v;
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = next_random(seed) % (i + 1);
        int64_t t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
}

int main(void) {
    const int64_t rounds = 100, count = 200, n = 100;
    int64_t seed = 969;
    static int64_t stacks[200][100];
    for (int64_t s = 0; s < count; s++) random_permutation(stacks[s], n, &seed);
    int64_t flips = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t s = 0; s < count; s++) {
            int64_t *f;
            int64_t len = pancake_sort(stacks[(r + s) % count], n, &f);
            for (int64_t j = 0; j < len; j++) {
                flips++;
                check = (check * 131 + f[j]) % 1000000007;
            }
            free(f);
        }
    }
    printf("%lld rounds over %lld stacks of 100 pancakes: %lld flips, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)flips, (long long)check);
    return 0;
}
