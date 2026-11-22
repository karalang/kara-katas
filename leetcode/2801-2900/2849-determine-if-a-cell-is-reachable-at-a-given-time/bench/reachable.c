// LeetCode #2849: Determine if a Cell Is Reachable at a Given Time --
// the bench: the ★ arm over 10^6 random cases on LeetCode's grid, the
// finish within 3 of the start and t within 2 of the distance, all
// drawn first, then each answered 20 times.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t sx, sy, fx, fy, t; } Case;

static int64_t labs64(int64_t x) { return x < 0 ? -x : x; }
static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }
static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static bool is_reachable_at_time(int64_t sx, int64_t sy, int64_t fx, int64_t fy, int64_t t) {
    if (sx == fx && sy == fy) return t != 1;
    return max64(labs64(sx - fx), labs64(sy - fy)) <= t;
}

static int64_t seed = 2849;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const long count = 1000000, rounds = 20;
    Case *cases = malloc(sizeof(Case) * count);
    for (long i = 0; i < count; i++) {
        int64_t sx = next_random() * 30000 % 1000000000 + 1;
        int64_t sy = next_random() * 30000 % 1000000000 + 1;
        int64_t fx = min64(max64(sx + next_random() % 7 - 3, 1), 1000000000);
        int64_t fy = sy;
        if (next_random() % 2 != 0) fy = min64(max64(sy + next_random() % 7 - 3, 1), 1000000000);
        int64_t d = max64(labs64(sx - fx), labs64(sy - fy));
        int64_t t = max64(d + next_random() % 5 - 2, 0);
        cases[i] = (Case){sx, sy, fx, fy, t};
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long i = 0; i < count; i++) {
            Case c = cases[i];
            bool ok = is_reachable_at_time(c.sx, c.sy, c.fx, c.fy, c.t);
            if (ok) yes++;
            check = (check * 3 + (ok ? 2 : 1) + r) % 1000000007;
        }
    }
    printf("%ld cases, %ld rounds: %lld true, checksum %lld\n", count, rounds, (long long)yes, (long long)check);
    free(cases);
    return 0;
}
