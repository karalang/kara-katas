// LeetCode #1503: Last Moment Before All Ants Fall Out of a Plank -- the
// benchmark, the same algorithm as ants.kara: the statement simulated with
// doubled positions and half-unit ticks.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t last_moment(int64_t n, const int64_t *left, int64_t nl, const int64_t *right, int64_t nr) {
    int64_t m = nl + nr;
    int64_t *pos = malloc((m + 1) * sizeof(int64_t));
    int64_t *dir = malloc((m + 1) * sizeof(int64_t));
    char *on = malloc(m + 1);
    for (int64_t i = 0; i < nl; i++) { pos[i] = 2 * left[i]; dir[i] = -1; }
    for (int64_t i = 0; i < nr; i++) { pos[nl + i] = 2 * right[i]; dir[nl + i] = 1; }
    memset(on, 1, m + 1);
    int64_t alive = m;
    int64_t *at = malloc((2 * n + 1) * sizeof(int64_t));
    for (int64_t i = 0; i <= 2 * n; i++) at[i] = -1;
    int64_t tick = 0, last = 0;
    while (alive > 0) {
        for (int64_t i = 0; i < m; i++) {
            if (on[i] && ((pos[i] == 0 && dir[i] == -1) || (pos[i] == 2 * n && dir[i] == 1))) {
                on[i] = 0;
                alive--;
                last = tick;
            }
        }
        for (int64_t i = 0; i < m; i++) {
            if (on[i]) {
                int64_t other = at[pos[i]];
                if (other >= 0) {
                    dir[i] = -dir[i];
                    dir[other] = -dir[other];
                } else {
                    at[pos[i]] = i;
                }
            }
        }
        for (int64_t i = 0; i < m; i++) {
            if (on[i]) {
                at[pos[i]] = -1;
                pos[i] += dir[i];
            }
        }
        tick++;
    }
    free(pos); free(dir); free(on); free(at);
    return last / 2;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

typedef struct { int64_t n, nl, nr; int64_t *left, *right; } Plank;

static Plank random_plank(int64_t most, int64_t *seed) {
    Plank p;
    p.n = next_random(seed) % most + 1;
    int64_t fill = next_random(seed) % 100 + 1;
    p.left = malloc((p.n + 1) * sizeof(int64_t));
    p.right = malloc((p.n + 1) * sizeof(int64_t));
    p.nl = p.nr = 0;
    for (int64_t q = 0; q <= p.n; q++) {
        if (next_random(seed) % 100 < fill) {
            if (next_random(seed) % 2 == 0) p.left[p.nl++] = q;
            else p.right[p.nr++] = q;
        }
    }
    return p;
}

int main(void) {
    int64_t seed = 1503;
    Plank planks[300];
    for (int i = 0; i < 300; i++) planks[i] = random_plank(1000, &seed);
    int64_t total = 0, check = 0;
    for (int i = 0; i < 300; i++) {
        int64_t answer = last_moment(planks[i].n, planks[i].left, planks[i].nl, planks[i].right, planks[i].nr);
        total += answer;
        check = mix(check, answer);
    }
    printf("300 planks of 1 to 1000 units simulated: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int i = 0; i < 300; i++) { free(planks[i].left); free(planks[i].right); }
    return 0;
}
