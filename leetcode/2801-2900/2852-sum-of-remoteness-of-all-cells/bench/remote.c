// LeetCode #2852: Sum of Remoteness of All Cells -- the bench: the ★ arm
// over 20 grids of 300 x 300, LeetCode's most, values up to 10^6, a
// cell blocked from 1 time in 10 to 6 in 10, all drawn first, then each
// answered 10 times. The queue is an array of n * n cells, which a
// region never outgrows, where the other languages grow a deque.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 300

static int64_t sum_remoteness(const int64_t *grid, int64_t n) {
    int64_t total = 0;
    for (int64_t k = 0; k < n * n; k++)
        if (grid[k] > 0) total += grid[k];
    bool *seen = calloc(n * n, sizeof(bool));
    int64_t *queue = malloc(sizeof(int64_t) * n * n);
    static const int64_t dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};
    int64_t answer = 0;
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = 0; j < n; j++) {
            if (grid[i * n + j] < 0 || seen[i * n + j]) continue;
            seen[i * n + j] = true;
            int64_t head = 0, tail = 0;
            queue[tail++] = i * n + j;
            int64_t size = 0, sum = 0;
            while (head < tail) {
                int64_t cell = queue[head++];
                int64_t r = cell / n, c = cell % n;
                size++;
                sum += grid[cell];
                for (int d = 0; d < 4; d++) {
                    int64_t nr = r + dr[d], nc = c + dc[d];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr * n + nc] > 0 && !seen[nr * n + nc]) {
                        seen[nr * n + nc] = true;
                        queue[tail++] = nr * n + nc;
                    }
                }
            }
            answer += size * (total - sum);
        }
    }
    free(seen);
    free(queue);
    return answer;
}

static int64_t seed = 2852;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 20, rounds = 10, n = N;
    int64_t *grids = malloc(sizeof(int64_t) * count * n * n);
    for (int64_t g = 0; g < count; g++) {
        int64_t blocked = next_random() % 6 + 1;
        for (int64_t k = 0; k < n * n; k++)
            grids[g * n * n + k] = next_random() % 10 < blocked ? -1 : wide() % 1000000 + 1;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int64_t g = 0; g < count; g++)
            check = (check * 31 + sum_remoteness(grids + g * n * n, n) % 1000000007 + r) % 1000000007;
    printf("%lld grids of %lld x %lld, %lld rounds: checksum %lld\n", (long long)count, (long long)n, (long long)n, (long long)rounds, (long long)check);
    free(grids);
    return 0;
}
