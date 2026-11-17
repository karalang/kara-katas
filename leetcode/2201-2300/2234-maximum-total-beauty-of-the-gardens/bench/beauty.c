// LeetCode #2234: Maximum Total Beauty of the Gardens -- the benchmark's
// C mirror of beauty.kara: every split of complete gardens tried, the
// level of the rest by a binary search on the level; qsort for the sort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int compare(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int64_t maximum_beauty(const int64_t *flowers, int64_t n, int64_t new_flowers, int64_t target, int64_t full, int64_t partial) {
    int64_t *sorted = malloc(n * sizeof *sorted);
    int64_t *prefix = malloc((n + 1) * sizeof *prefix);
    for (int64_t i = 0; i < n; i++) sorted[i] = flowers[i] < target ? flowers[i] : target;
    qsort(sorted, n, sizeof *sorted, compare);
    prefix[0] = 0;
    for (int64_t i = 0; i < n; i++) prefix[i + 1] = prefix[i] + sorted[i];
    int64_t best = 0, cost = 0;
    for (int64_t c = n; c >= 0; c--) {
        if (c < n) cost += target - sorted[c];
        if (cost > new_flowers) break;
        int64_t complete = (n - c) * full;
        if (c == 0) {
            if (complete > best) best = complete;
        } else if (sorted[c - 1] < target) {
            int64_t left = new_flowers - cost;
            int64_t low = sorted[0], high = target - 1;
            while (low < high) {
                int64_t m = (low + high + 1) / 2;
                int64_t a = 0, b = c;
                while (a < b) {
                    int64_t mid = (a + b) / 2;
                    if (sorted[mid] < m) a = mid + 1;
                    else b = mid;
                }
                if (m * a - prefix[a] <= left) low = m;
                else high = m - 1;
            }
            if (complete + low * partial > best) best = complete + low * partial;
        }
    }
    free(sorted);
    free(prefix);
    return best;
}

static int64_t seed = 2234;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t n = 20000;
    int64_t *flowers = malloc(n * sizeof *flowers);
    for (int64_t i = 0; i < n; i++) flowers[i] = wide_random() % 100000 + 1;
    int64_t check = 0;
    for (int pass = 0; pass < 20; pass++) {
        // punch: one garden drawn again before each pass, and the new
        // flowers drawn anew
        int64_t at = next_random() % 20000;
        flowers[at] = wide_random() % 100000 + 1;
        int64_t new_flowers = wide_random() % 1200000000 + 1;
        check = (check * 31 + maximum_beauty(flowers, n, new_flowers, 100000, 100000, 100000)) % 1000000007;
    }
    printf("20 passes over 20000 gardens: checksum %lld\n", (long long)check);
    free(flowers);
    return 0;
}
