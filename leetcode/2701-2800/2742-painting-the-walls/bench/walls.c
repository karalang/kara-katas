// LeetCode #2742: Painting the Walls -- the bench (walls.kara in C): a
// knapsack over the walls covered.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t paint_walls(const int64_t *cost, const int64_t *time, int64_t n) {
    int64_t far = INT64_MAX / 2;
    int64_t *least = malloc(sizeof(int64_t) * (n + 1));
    for (int64_t j = 0; j <= n; j++) least[j] = far;
    least[0] = 0;
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = n; j >= 1; j--) {
            int64_t from = j - time[i] - 1;
            if (from < 0) from = 0;
            if (least[from] + cost[i] < least[j]) least[j] = least[from] + cost[i];
        }
    }
    int64_t answer = least[n];
    free(least);
    return answer;
}

static int64_t seed = 2742;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 20, n = 500, rounds = 100;
    int64_t *costs = malloc(sizeof(int64_t) * count * n);
    int64_t *times = malloc(sizeof(int64_t) * count * n);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) {
            int64_t hi = next_random();
            int64_t lo = next_random();
            costs[c * n + i] = (hi * 32768 + lo) % 1000000 + 1;
        }
        for (int64_t i = 0; i < n; i++) times[c * n + i] = next_random() % 20 + 1;
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t least = paint_walls(costs + c * n, times + c * n, n);
            sum += least;
            check = (check * 31 + least + r) % 1000000007;
        }
    }
    printf("%lld cases of %lld walls, %lld rounds: costs sum to %lld, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)sum, (long long)check);
    free(costs);
    free(times);
    return 0;
}
