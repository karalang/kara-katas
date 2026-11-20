// LeetCode #2398: Maximum Number of Robots Within Budget -- the bench, the
// ★ arm in C: a sliding window, its largest charge time kept by a
// monotonic deque in a ring of indexes.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 50000

static int64_t seed = 2398;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

static int64_t maximum_robots(const int64_t *charge, const int64_t *running, int64_t n, int64_t budget) {
    int64_t *largest = malloc(sizeof(int64_t) * n);
    int64_t head = 0, tail = 0;
    int64_t best = 0, left = 0, sum = 0;
    for (int64_t right = 0; right < n; right++) {
        sum += running[right];
        while (tail > head && charge[largest[tail - 1]] <= charge[right]) tail--;
        largest[tail++] = right;
        while (left <= right && charge[largest[head]] + (right - left + 1) * sum > budget) {
            if (largest[head] == left) head++;
            sum -= running[left];
            left++;
        }
        if (right - left + 1 > best) best = right - left + 1;
    }
    free(largest);
    return best;
}

int main(void) {
    static int64_t charge[20][N], running[20][N];
    for (int f = 0; f < 20; f++) {
        for (int i = 0; i < N; i++) charge[f][i] = 1 + wide() % 100000;
        for (int i = 0; i < N; i++) running[f][i] = 1 + wide() % 100000;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 2; p++) {
        for (int f = 0; f < 20; f++) {
            for (int64_t budget = 100000; budget <= 1000000000000000LL; budget *= 10)
                check = (check * 31 + maximum_robots(charge[f], running[f], N, budget) + p) % 1000000007;
        }
    }
    printf("2 passes over 20 fleets of 5 * 10^4 robots, 11 budgets: checksum %lld\n", (long long)check);
    return 0;
}
