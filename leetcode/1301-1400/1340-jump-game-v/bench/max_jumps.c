// LeetCode #1340 bench in C: the ★ arm (memoized depth-first search, each
// direction walked outward up to d steps and stopped at the first value
// not lower) on the same 20 arrays of 1000 values and 20 passes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int most_from(const int *arr, int n, int d, int i, int *memo) {
    if (memo[i] > 0) return memo[i];
    int best = 1;
    for (int step = -1; step <= 1; step += 2) {
        int j = i + step;
        while (j >= 0 && j < n && abs(j - i) <= d && arr[j] < arr[i]) {
            int m = 1 + most_from(arr, n, d, j, memo);
            if (m > best) best = m;
            j += step;
        }
    }
    memo[i] = best;
    return best;
}

static int max_jumps(const int *arr, int n, int d) {
    int *memo = calloc((size_t)n, sizeof(int));
    int best = 0;
    for (int i = 0; i < n; i++) {
        int m = most_from(arr, n, d, i, memo);
        if (m > best) best = m;
    }
    free(memo);
    return best;
}

static int64_t seed = 1340;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { N = 1000 };
    static int arrays[20][N];
    for (int a = 0; a < 20; a++) {
        for (int k = 0; k < N; k++) {
            if (a % 2 == 0) arrays[a][k] = (int)(1 + next_random() % 100000);
            else arrays[a][k] = (int)(100 * k + 1 + next_random() % 100);
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 20; pass++) {
        for (int a = 0; a < 20; a++) {
            arrays[a][check % N] = (int)(1 + (check / 7) % 100000);
            int d = a % 2 == 0 ? 1000 : 300;
            int answer = max_jumps(arrays[a], N, d);
            check = (check * 31 + answer + pass) % 1000000007;
        }
    }
    printf("20 passes over 20 arrays of 1000: checksum %lld\n", (long long)check);
    return 0;
}
