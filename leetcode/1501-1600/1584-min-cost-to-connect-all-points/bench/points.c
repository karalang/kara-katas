// LeetCode #1584 bench: the same Prim's algorithm with no edge list, in C.
// Every point is its own allocation, as in the Kara Vec[Vec[i64]]; the
// distinctness check is a linear scan, as the sets elsewhere cost little
// beside the O(n^2) solve.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_cost_connect_points(int64_t **points, int64_t n) {
    int64_t *nearest = malloc(n * sizeof(int64_t));
    char *inside = calloc(n, 1);
    for (int64_t i = 0; i < n; i++) nearest[i] = INT64_MAX;
    nearest[0] = 0;
    int64_t cost = 0;
    for (int64_t k = 0; k < n; k++) {
        int64_t next = -1;
        for (int64_t i = 0; i < n; i++)
            if (!inside[i] && (next < 0 || nearest[i] < nearest[next])) next = i;
        inside[next] = 1;
        cost += nearest[next];
        for (int64_t i = 0; i < n; i++) {
            if (!inside[i]) {
                int64_t dx = points[i][0] - points[next][0], dy = points[i][1] - points[next][1];
                int64_t d = (dx < 0 ? -dx : dx) + (dy < 0 ? -dy : dy);
                if (d < nearest[i]) nearest[i] = d;
            }
        }
    }
    free(nearest);
    free(inside);
    return cost;
}

static int64_t seed = 1584;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    enum { P = 100, N = 1000 };
    int64_t **problems[P];
    for (int p = 0; p < P; p++) {
        problems[p] = malloc(N * sizeof(int64_t *));
        int64_t n = 0;
        while (n < N) {
            int64_t x = (next_random() * 32768 + next_random()) % 2000001 - 1000000;
            int64_t y = (next_random() * 32768 + next_random()) % 2000001 - 1000000;
            int fresh = 1;
            for (int64_t i = 0; i < n; i++)
                if (problems[p][i][0] == x && problems[p][i][1] == y) fresh = 0;
            if (fresh) {
                int64_t *pt = malloc(2 * sizeof(int64_t));
                pt[0] = x;
                pt[1] = y;
                problems[p][n++] = pt;
            }
        }
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < P; p++) {
        int64_t cost = min_cost_connect_points(problems[p], N);
        total += cost;
        check = mix(check, cost);
    }
    printf("100 problems of 1000 points: cost %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int p = 0; p < P; p++) {
        for (int i = 0; i < N; i++) free(problems[p][i]);
        free(problems[p]);
    }
    return 0;
}
