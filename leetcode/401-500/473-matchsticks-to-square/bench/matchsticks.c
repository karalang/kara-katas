// Benchmark for #473: C mirror of the ★ arm (backtracking, longest stick
// first); see matchsticks.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool place(const int64_t *sticks, int n, int i, int64_t *sides, int64_t side) {
    if (i == n) {
        return true;
    }
    for (int s = 0; s < 4; s++) {
        if (sides[s] + sticks[i] > side) {
            continue;
        }
        bool repeat = false;
        for (int t = 0; t < s; t++) {
            if (sides[t] == sides[s]) {
                repeat = true;
                break;
            }
        }
        if (repeat) {
            continue;
        }
        sides[s] += sticks[i];
        if (place(sticks, n, i + 1, sides, side)) {
            return true;
        }
        sides[s] -= sticks[i];
    }
    return false;
}

static int cmp_desc(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x < y) - (x > y);
}

static bool makesquare(const int64_t *matchsticks, int n) {
    if (n < 4) {
        return false;
    }
    int64_t total = 0;
    for (int i = 0; i < n; i++) {
        total += matchsticks[i];
    }
    if (total % 4 != 0) {
        return false;
    }
    int64_t side = total / 4;
    int64_t *sticks = malloc(sizeof(int64_t) * n);
    for (int i = 0; i < n; i++) {
        sticks[i] = matchsticks[i];
    }
    qsort(sticks, n, sizeof(int64_t), cmp_desc);
    bool ok = false;
    if (sticks[0] <= side) {
        int64_t sides[4] = {0, 0, 0, 0};
        ok = place(sticks, n, 0, sides, side);
    }
    free(sticks);
    return ok;
}

static int64_t seed = 473;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int cases = 2000;
    int squares = 0;
    int64_t checksum = 0;
    for (int c = 0; c < cases; c++) {
        int64_t sticks[15];
        int64_t total = 0;
        for (int i = 0; i < 15; i++) {
            int64_t v = 50 + next_random() % 50;
            sticks[i] = v;
            total += v;
        }
        sticks[14] += (4 - total % 4) % 4;
        bool ok = makesquare(sticks, 15);
        if (ok) {
            squares++;
        }
        checksum = (checksum * 3 + (ok ? 1 : 2)) % 1000000007;
    }
    printf("%d sets of 15 sticks: %d squares, checksum %lld\n", cases, squares, (long long)checksum);
    return 0;
}
