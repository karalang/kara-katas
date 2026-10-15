// LeetCode #683: K Empty Slots -- a window over the days. Bench.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 100
#define N 20000
#define ROUNDS 30

static int64_t seed = 683;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t k_empty_slots(const int64_t *bulbs, int64_t n, int64_t k) {
    int64_t *days = malloc(sizeof(int64_t) * n);
    for (int64_t d = 0; d < n; d++) days[bulbs[d] - 1] = d + 1;
    int64_t best = -1, left = 0, right = k + 1, i = 1;
    while (right < n) {
        if (i == right) {
            int64_t day = days[left] > days[right] ? days[left] : days[right];
            if (best == -1 || day < best) best = day;
            left = right;
            right = left + k + 1;
            i = left + 1;
        } else if (days[i] < days[left] || days[i] < days[right]) {
            left = i;
            right = left + k + 1;
            i = left + 1;
        } else {
            i++;
        }
    }
    free(days);
    return best;
}

int main(void) {
    static int64_t orders[COUNT][N];
    for (int64_t c = 0; c < COUNT; c++) {
        for (int64_t x = 0; x < N; x++) orders[c][x] = x + 1;
        for (int64_t i = N - 1; i > 0; i--) {
            int64_t a = next_random();
            int64_t j = (a * 32768 + next_random()) % (i + 1);
            int64_t t = orders[c][i];
            orders[c][i] = orders[c][j];
            orders[c][j] = t;
        }
    }
    int64_t sum = 0, none = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t c = 0; c < COUNT; c++) {
            int64_t k = (c * 7 + r) % 50;
            int64_t day = k_empty_slots(orders[c], N, k);
            if (day == -1) none++;
            sum = (sum * 31 + day + 2) % 1000000007;
        }
    }
    printf("%d answers: %lld without a day, checksum %lld\n", COUNT * ROUNDS,
           (long long)none, (long long)sum);
    return 0;
}
