// LeetCode #2106: Maximum Fruits Harvested After at Most K Steps --
// bench, C mirror of harvest.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t steps(int64_t l, int64_t r, int64_t start) {
    if (l >= start) return r - start;
    if (r <= start) return start - l;
    int64_t a = 2 * (start - l) + (r - start), b = (start - l) + 2 * (r - start);
    return a < b ? a : b;
}

static int64_t max_total_fruits(const int64_t *pos, const int64_t *amt, int64_t n, int64_t start, int64_t k) {
    int64_t left = 0, sum = 0, best = 0;
    for (int64_t right = 0; right < n; right++) {
        sum += amt[right];
        while (left <= right && steps(pos[left], pos[right], start) > k) {
            sum -= amt[left];
            left++;
        }
        if (sum > best) best = sum;
    }
    return best;
}

static int64_t seed = 2106;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

int main(void) {
    int64_t *pos[20], *amt[20], len[20];
    for (int f = 0; f < 20; f++) {
        pos[f] = malloc(sizeof(int64_t) * 200000);
        amt[f] = malloc(sizeof(int64_t) * 200000);
        len[f] = 0;
        for (int64_t p = 0; p < 200000; p++) {
            if (next_random() % 2 == 0) {
                pos[f][len[f]] = p;
                amt[f][len[f]] = wide_random() % 10000 + 1;
                len[f]++;
            }
        }
    }
    int64_t total = 0, check = 0;
    for (int f = 0; f < 20; f++)
        for (int q = 0; q < 10; q++) {
            int64_t start = wide_random() % 200001;
            int64_t k = wide_random() % 200001;
            int64_t got = max_total_fruits(pos[f], amt[f], len[f], start, k);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    printf("200 walks: %lld fruits, checksum %lld\n", (long long)total, (long long)check);
    for (int f = 0; f < 20; f++) {
        free(pos[f]);
        free(amt[f]);
    }
    return 0;
}
