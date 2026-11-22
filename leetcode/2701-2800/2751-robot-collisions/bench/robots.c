// LeetCode #2751: Robot Collisions -- the bench (robots.kara in C): the
// robots in order of position by `qsort`, those moving right on a stack,
// and each robot moving left meeting the stack's top in turn.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static const int64_t *sort_positions;

static int by_position(const void *a, const void *b) {
    int64_t x = sort_positions[*(const int64_t *)a], y = sort_positions[*(const int64_t *)b];
    return (x > y) - (x < y);
}

// writes the survivors into `out` and returns how many
static int64_t survived_robots_healths(const int64_t *positions, const int64_t *healths, const char *directions, int64_t n, int64_t *out) {
    int64_t *health = malloc(sizeof(int64_t) * n);
    int64_t *order = malloc(sizeof(int64_t) * n);
    int64_t *stack = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) { health[i] = healths[i]; order[i] = i; }
    sort_positions = positions;
    qsort(order, n, sizeof(int64_t), by_position);
    int64_t top_at = 0;
    for (int64_t k = 0; k < n; k++) {
        int64_t i = order[k];
        if (directions[i] == 'R') { stack[top_at++] = i; continue; }
        while (health[i] > 0 && top_at > 0) {
            int64_t top = stack[top_at - 1];
            if (health[top] < health[i]) { health[top] = 0; top_at--; health[i]--; }
            else if (health[top] > health[i]) { health[top]--; health[i] = 0; }
            else { health[top] = 0; top_at--; health[i] = 0; }
        }
    }
    int64_t m = 0;
    for (int64_t i = 0; i < n; i++) if (health[i] > 0) out[m++] = health[i];
    free(health); free(order); free(stack);
    return m;
}

static int64_t seed = 2751;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 10, rounds = 3;
    int64_t (*positions)[N] = malloc(sizeof(int64_t) * count * N);
    int64_t (*healths)[N] = malloc(sizeof(int64_t) * count * N);
    char (*directions)[N] = malloc((size_t)count * N);
    for (int k = 0; k < count; k++) {
        for (int64_t i = 0; i < N; i++) positions[k][i] = i * 10000 + next_random() % 10000 + 1;
        for (int64_t i = N - 1; i >= 1; i--) {
            int64_t hi = next_random();
            int64_t j = (hi * 32768 + next_random()) % (i + 1);
            int64_t t = positions[k][i]; positions[k][i] = positions[k][j]; positions[k][j] = t;
        }
        for (int64_t i = 0; i < N; i++) {
            int64_t hi = next_random();
            healths[k][i] = (hi * 32768 + next_random()) % 1000000000 + 1;
        }
        for (int64_t i = 0; i < N; i++) directions[k][i] = next_random() % 2 == 0 ? 'L' : 'R';
    }
    int64_t *out = malloc(sizeof(int64_t) * N);
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < count; k++) {
            int64_t m = survived_robots_healths(positions[k], healths[k], directions[k], N, out);
            check = (check * 31 + m + r) % 1000000007;
            for (int64_t i = 0; i < m; i++) {
                sum += out[i];
                check = (check * 31 + out[i]) % 1000000007;
            }
        }
    printf("%d cases of 100000 robots, %d rounds: healths sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(positions); free(healths); free(directions); free(out);
    return 0;
}
