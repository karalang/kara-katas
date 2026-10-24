// Benchmark: LeetCode #948 Bag of Tokens -- the ★ arm, sorted and played
// from both ends, on bags of 1000 tokens, LeetCode's largest. Mirrors
// bag_of_tokens_score.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1000
#define COUNT 20

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t bag_of_tokens_score(const int64_t *tokens, int64_t n, int64_t power) {
    int64_t *t = malloc(sizeof(int64_t) * (size_t)n);
    memcpy(t, tokens, sizeof(int64_t) * (size_t)n);
    qsort(t, (size_t)n, sizeof(int64_t), cmp_i64);
    int64_t lo = 0, hi = n - 1, p = power, score = 0, best = 0;
    while (lo <= hi) {
        if (p >= t[lo]) {
            p -= t[lo];
            lo++;
            score++;
            if (score > best) best = score;
        } else if (score > 0 && lo < hi) {
            p += t[hi];
            hi--;
            score--;
        } else {
            break;
        }
    }
    free(t);
    return best;
}

static int64_t seed = 948;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t bags[COUNT][N];
static int64_t powers[COUNT];

int main(void) {
    const int64_t rounds = 500, count = COUNT, n = N;
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) bags[c][i] = next_random() % 10000;
        powers[c] = next_random() % 10000;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t b = (r + i) % count;
            int64_t s = bag_of_tokens_score(bags[b], n, powers[b]);
            total += s;
            check = (check * 1000003 + s) % 1000000007;
        }
    }
    printf("%lld rounds over %lld bags of %lld tokens: scores adding to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)total, (long long)check);
    return 0;
}
