// Benchmark for #528: C mirror of the ★ arm (prefix sums and a binary
// search); see random_pick_with_weight.kara. The same seeded generator,
// so the same picks; a fresh prefix-sum array per solution, as the ★
// arm's `Vec`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t seed;
} Draw;

static int64_t step(Draw *d) {
    d->seed = (d->seed * 1103515245 + 12345) % 2147483648LL;
    return d->seed / 65536;
}

static int64_t below(Draw *d, int64_t n) {
    int64_t limit = 1073741824 / n * n;
    for (;;) {
        int64_t high = step(d);
        int64_t low = step(d);
        int64_t r = high * 32768 + low;
        if (r < limit) return r % n;
    }
}

typedef struct {
    int64_t *ends;
    int64_t n;
    Draw draw;
} Solution;

static Solution solution_new(const int64_t *w, int64_t n, int64_t seed) {
    Solution s = {malloc(n * sizeof(int64_t)), n, {seed}};
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        total += w[i];
        s.ends[i] = total;
    }
    return s;
}

static int64_t pick_index(Solution *s) {
    int64_t r = below(&s->draw, s->ends[s->n - 1]);
    int64_t low = 0, high = s->n - 1;
    while (low < high) {
        int64_t mid = (low + high) / 2;
        if (s->ends[mid] > r) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return low;
}

int main(void) {
    int64_t seed = 528;
    int64_t *lists[20];
    for (int l = 0; l < 20; l++) {
        lists[l] = malloc(10000 * sizeof(int64_t));
        for (int i = 0; i < 10000; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int64_t high = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            lists[l][i] = 1 + (high * 32768 + seed / 65536) % 100000;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < 50; round++) {
        for (int64_t l = 0; l < 20; l++) {
            Solution s = solution_new(lists[l], 10000, round * 20 + l);
            for (int k = 0; k < 10000; k++) {
                int64_t i = pick_index(&s);
                total += i;
                checksum = (checksum * 31 + i) % 1000000007;
            }
            free(s.ends);
        }
    }
    printf("20 lists of 10000, 50 rounds of 10000 picks: total %lld, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}
