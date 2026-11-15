// LeetCode #1578 bench: the same one pass, in C. Each rope's colours and
// times are grown by doubling, as the Kara String and Vec are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char *colors;
    int64_t *times;
    int64_t n;
} Rope;

static int64_t min_cost(const char *cs, const int64_t *needed_time, int64_t n) {
    int64_t total = 0, keep = 0;
    for (int64_t i = 0; i < n; i++) {
        if (i > 0 && cs[i] != cs[i - 1]) keep = 0;
        total += keep < needed_time[i] ? keep : needed_time[i];
        keep = keep > needed_time[i] ? keep : needed_time[i];
    }
    return total;
}

static int64_t seed = 1578;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    Rope ropes[200];
    for (int r = 0; r < 200; r++) {
        int64_t cap_c = 8, cap_t = 4, n = 0;
        char *colors = malloc(cap_c);
        int64_t *times = malloc(cap_t * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) {
            if (n == cap_c) colors = realloc(colors, cap_c *= 2);
            colors[n] = (char)('a' + next_random() % 3);
            if (n == cap_t) times = realloc(times, (cap_t *= 2) * sizeof(int64_t));
            times[n] = next_random() % 1000 + 1;
            n++;
        }
        ropes[r] = (Rope){colors, times, n};
    }
    int64_t check = 0, total = 0;
    for (int r = 0; r < 200; r++) {
        int64_t cost = min_cost(ropes[r].colors, ropes[r].times, ropes[r].n);
        total += cost;
        check = mix(check, cost);
    }
    printf("200 ropes of 100000 balloons: time total %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int r = 0; r < 200; r++) {
        free(ropes[r].colors);
        free(ropes[r].times);
    }
    return 0;
}
