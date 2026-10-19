// LeetCode 798 — Smallest Rotation with Highest Score: the bench, in C.
// Mirrors best_rotation.kara: a difference array over the rotations.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t best_rotation(const int64_t *nums, int64_t n) {
    int64_t *change = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t first = (i + 1) % n;
        int64_t last = (i - nums[i] + n) % n;
        change[first] += 1;
        change[last + 1] -= 1;
        if (first > last) {
            change[0] += 1;
            change[n] -= 1;
        }
    }
    int64_t best = 0, best_score = -1, score = 0;
    for (int64_t k = 0; k < n; k++) {
        score += change[k];
        if (score > best_score) {
            best_score = score;
            best = k;
        }
    }
    free(change);
    return best;
}

static int64_t seed = 798;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int64_t *arrays[16];
    for (int a = 0; a < 16; a++) {
        int64_t hi = next_random();
        int64_t top = 1 + (hi * 32768 + next_random()) % n;
        arrays[a] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            int64_t h = next_random();
            arrays[a][i] = (h * 32768 + next_random()) % top;
        }
    }
    const int64_t rounds = 4000;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t k = best_rotation(arrays[r % 16], n);
        total += k;
        check = (check * 131 + k) % 1000000007;
    }
    printf("%lld rounds of %lld numbers: rotations adding up to %lld, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)check);
    return 0;
}
