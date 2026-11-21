// LeetCode #2511: Maximum Enemy Forts That Can Be Captured -- C mirror of
// the benchmark (forts.kara): the same lines, passes and checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t capture_forts(const int64_t *forts, int64_t n) {
    int64_t best = 0, last = -1;
    for (int64_t i = 0; i < n; i++) {
        if (forts[i] != 0) {
            if (last >= 0 && forts[last] == -forts[i] && i - last - 1 > best) best = i - last - 1;
            last = i;
        }
    }
    return best;
}

static int64_t seed = 2511;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *lines = malloc(2000 * 1000 * sizeof *lines);
    for (int64_t k = 0; k < 2000; k++) {
        int64_t zeros = k % 50 + 1;
        for (int64_t i = 0; i < 1000; i++) {
            int64_t r = next_random() % (zeros + 2);
            lines[k * 1000 + i] = r < zeros ? 0 : (r == zeros ? 1 : -1);
        }
    }
    const int64_t passes = 115;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int64_t k = 0; k < 2000; k++) {
            int64_t *line = lines + k * 1000;
            int64_t at = check % 1000;
            int64_t kept = line[at];
            line[at] = (check + p) % 3 - 1;
            check = (check * 31 + capture_forts(line, 1000) + p) % 1000000007;
            line[at] = kept;
        }
    }
    printf("%lld passes over 2000 lines of 1000 forts: checksum %lld\n", (long long)passes, (long long)check);
    free(lines);
    return 0;
}
