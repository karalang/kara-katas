// LeetCode #1499: Max Value of Equation -- the bench in C, mirroring
// find_max_value_of_equation.kara: a window of (y - x, x) kept largest first,
// here a ring buffer the size of the points.
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 200000

static int find_max_value_of_equation(int (*points)[2], int n, int k, int (*window)[2]) {
    int head = 0, tail = 0;
    int best = INT_MIN;
    for (int i = 0; i < n; i++) {
        int x = points[i][0], y = points[i][1];
        while (head < tail && x - window[head][1] > k) head++;
        if (head < tail && window[head][0] + y + x > best) best = window[head][0] + y + x;
        while (head < tail && window[tail - 1][0] <= y - x) tail--;
        window[tail][0] = y - x;
        window[tail][1] = x;
        tail++;
    }
    return best;
}

int main(void) {
    int64_t seed = 1499;
    int (*points)[2] = malloc(sizeof(int[2]) * N);
    int (*window)[2] = malloc(sizeof(int[2]) * N);
    int64_t x = 0;
    for (int i = 0; i < N; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        x += 1 + seed / 65536 % 10;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t y = seed / 65536 * 6151 % 200000001 - 100000000;
        points[i][0] = (int)x;
        points[i][1] = (int)y;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 400; call++) {
        int64_t at = (check + call * 7919) % N;
        points[at][1] = (int)((check * 17 + call) % 200000001 - 100000000);
        int64_t k = 10 + (check + call) % 2000;
        check = (check * 31 + find_max_value_of_equation(points, N, (int)k, window) + 300000000) % 1000000007;
    }
    printf("400 calls over 200000 points: checksum %lld\n", (long long)check);
    free(points);
    free(window);
    return 0;
}
