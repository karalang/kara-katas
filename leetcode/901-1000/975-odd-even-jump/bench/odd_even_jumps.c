// Benchmark: LeetCode #975 Odd Even Jump -- the stack arm (sorted order
// and a monotonic stack), on 20 arrays of 20000 random values. Mirrors
// odd_even_jumps.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 20000
#define COUNT 20

static const int64_t *keyed;

static int by_up(const void *a, const void *b) {
    int64_t i = *(const int64_t *)a, j = *(const int64_t *)b;
    if (keyed[i] != keyed[j]) return keyed[i] < keyed[j] ? -1 : 1;
    return (i > j) - (i < j);
}

static int by_down(const void *a, const void *b) {
    int64_t i = *(const int64_t *)a, j = *(const int64_t *)b;
    if (keyed[i] != keyed[j]) return keyed[i] > keyed[j] ? -1 : 1;
    return (i > j) - (i < j);
}

static void next_in(const int64_t *order, int64_t n, int64_t *next) {
    int64_t *stack = malloc((size_t)n * sizeof(int64_t));
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) next[i] = -1;
    for (int64_t k = 0; k < n; k++) {
        int64_t i = order[k];
        while (top > 0 && stack[top - 1] < i) next[stack[--top]] = i;
        stack[top++] = i;
    }
    free(stack);
}

static int64_t odd_even_jumps(const int64_t *arr, int64_t n) {
    int64_t *up = malloc((size_t)n * sizeof(int64_t));
    int64_t *down = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) up[i] = down[i] = i;
    keyed = arr;
    qsort(up, (size_t)n, sizeof(int64_t), by_up);
    qsort(down, (size_t)n, sizeof(int64_t), by_down);
    int64_t *odd = malloc((size_t)n * sizeof(int64_t));
    int64_t *even = malloc((size_t)n * sizeof(int64_t));
    next_in(up, n, odd);
    next_in(down, n, even);
    char *higher = calloc((size_t)n, 1), *lower = calloc((size_t)n, 1);
    higher[n - 1] = lower[n - 1] = 1;
    for (int64_t i = n - 2; i >= 0; i--) {
        if (odd[i] >= 0) higher[i] = lower[odd[i]];
        if (even[i] >= 0) lower[i] = higher[even[i]];
    }
    int64_t good = 0;
    for (int64_t i = 0; i < n; i++) good += higher[i];
    free(up); free(down); free(odd); free(even); free(higher); free(lower);
    return good;
}

static int64_t seed = 975;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t arrays[COUNT][N];

int main(void) {
    int64_t rounds = 10;
    for (int c = 0; c < COUNT; c++)
        for (int i = 0; i < N; i++) arrays[c][i] = next_random() % 100000;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < COUNT; i++) {
            int64_t good = odd_even_jumps(arrays[(r + i) % COUNT], N);
            total += good;
            check = (check * 31 + good) % 1000000007;
        }
    }
    printf("%lld rounds over %d arrays of 20000 values: %lld good starts, checksum %lld\n",
           (long long)rounds, COUNT, (long long)total, (long long)check);
    return 0;
}
