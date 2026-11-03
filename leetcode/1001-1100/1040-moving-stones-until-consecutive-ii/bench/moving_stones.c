// Benchmark lane for LeetCode 1040 -- C mirror of moving_stones.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static void moves(const int64_t *stones, int64_t n, int64_t *least_out, int64_t *most_out) {
    int64_t *s = malloc(n * sizeof(int64_t));
    memcpy(s, stones, n * sizeof(int64_t));
    qsort(s, n, sizeof(int64_t), cmp);
    int64_t a = s[n - 1] - s[1] - n + 2, b = s[n - 2] - s[0] - n + 2;
    int64_t most = a > b ? a : b;
    int64_t least = n;
    int64_t i = 0;
    for (int64_t j = 0; j < n; j++) {
        while (s[j] - s[i] >= n) i++;
        int64_t inside = j - i + 1;
        int64_t cost = (inside == n - 1 && s[j] - s[i] == n - 2) ? 2 : n - inside;
        if (cost < least) least = cost;
    }
    free(s);
    *least_out = least;
    *most_out = most;
}

static int64_t seed = 1040;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t draw(int64_t top) {
    int64_t a = next_random();
    int64_t b = next_random();
    return (a * 32768 + b) % top;
}

int main(void) {
    const int count = 400, rounds = 5;
    const int64_t size = 10000;
    int64_t *sets = malloc(count * size * sizeof(int64_t));
    for (int c = 0; c < count; c++) {
        int64_t widest = c % 2 == 0 ? 100000 : 3;
        int64_t *stones = sets + c * size;
        int64_t at = 0;
        for (int64_t k = 0; k < size; k++) {
            at += draw(widest) + 1;
            stones[k] = at;
        }
        for (int64_t i = size - 1; i > 0; i--) {
            int64_t j = draw(i + 1);
            int64_t keep = stones[i];
            stones[i] = stones[j];
            stones[j] = keep;
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            int64_t least, most;
            moves(sets + c * size, size, &least, &most);
            total += least + most;
            check = (check * 131 + least * 1000003 + most) % 1000000007;
        }
    }
    printf("%d sets of %lld stones, %d rounds: total %lld, checksum %lld\n", count, (long long)size, rounds,
           (long long)total, (long long)check);
    free(sets);
    return 0;
}
