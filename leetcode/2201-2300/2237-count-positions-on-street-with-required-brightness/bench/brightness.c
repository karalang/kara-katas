// LeetCode #2237: Count Positions on Street With Required Brightness --
// the benchmark's C mirror of brightness.kara: a difference array, a
// running sum, and the positions meeting their requirement counted.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t meet_requirement(int64_t n, int64_t (*lights)[2], int64_t m, const int64_t *requirement) {
    int64_t *change = calloc(n + 1, sizeof *change);
    for (int64_t k = 0; k < m; k++) {
        int64_t from = lights[k][0] - lights[k][1];
        if (from < 0) from = 0;
        int64_t to = lights[k][0] + lights[k][1];
        if (to > n - 1) to = n - 1;
        change[from] += 1;
        change[to + 1] -= 1;
    }
    int64_t brightness = 0, count = 0;
    for (int64_t i = 0; i < n; i++) {
        brightness += change[i];
        if (brightness >= requirement[i]) count++;
    }
    free(change);
    return count;
}

static int64_t seed = 2237;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t n = 100000, m = 100000;
    int64_t (*lights)[2] = malloc(m * sizeof *lights);
    int64_t *requirement = malloc(n * sizeof *requirement);
    for (int64_t k = 0; k < m; k++) {
        int64_t position = wide_random() % n;
        lights[k][0] = position;
        lights[k][1] = wide_random() % 1001;
    }
    for (int64_t i = 0; i < n; i++) requirement[i] = wide_random() % 2001;
    int64_t check = 0;
    for (int pass = 0; pass < 100; pass++) {
        // punch: one light and one requirement drawn again before each pass
        int64_t at = wide_random() % 100000;
        int64_t position = wide_random() % n;
        int64_t range = wide_random() % 1001;
        lights[at][0] = position;
        lights[at][1] = range;
        int64_t place = wide_random() % n;
        requirement[place] = wide_random() % 2001;
        check = (check * 31 + meet_requirement(n, lights, m, requirement)) % 1000000007;
    }
    printf("100 passes over 10^5 positions and lights: checksum %lld\n", (long long)check);
    free(lights);
    free(requirement);
    return 0;
}
