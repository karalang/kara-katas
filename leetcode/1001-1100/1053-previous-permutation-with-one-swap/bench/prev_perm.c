// LeetCode #1053: Previous Permutation With One Swap -- C mirror of
// bench/prev_perm.kara.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long seed = 1053;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// The answer is written to `out`, a fresh copy of `arr`.
static void prev_perm_opt1(const long long *arr, long long n, long long *out) {
    memcpy(out, arr, sizeof(long long) * n);
    long long i = n - 2;
    while (i >= 0 && out[i] <= out[i + 1]) i--;
    if (i < 0) return;
    long long j = n - 1;
    while (out[j] >= out[i]) j--;
    while (out[j - 1] == out[j]) j--;
    long long t = out[i];
    out[i] = out[j];
    out[j] = t;
}

int main(void) {
    enum { COUNT = 200, N = 20000, ROUNDS = 25 };
    long long *all = malloc(sizeof(long long) * COUNT * N);
    long long from[COUNT];
    for (int a = 0; a < COUNT; a++) {
        long long run = next_random() % (N - 1) + 1;
        long long *arr = all + (long long)a * N;
        long long k = 0;
        for (; k < N - run; k++) arr[k] = next_random() % 10000 + 1;
        long long v = next_random() % 1000 + 1;
        for (long long r = 0; r < run; r++) {
            arr[k++] = v;
            v += next_random() % 3;
        }
        from[a] = N - run - 1;
    }
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int a = 0; a < COUNT; a++) {
            long long *answer = malloc(sizeof(long long) * N);
            prev_perm_opt1(all + (long long)a * N, N, answer);
            long long h = 0;
            for (long long k = from[a]; k < N; k++) h = (h * 10007 + answer[k]) % 1000000007;
            total += answer[from[a]];
            check = (check * 131 + h) % 1000000007;
            free(answer);
        }
    }
    printf("%d arrays of %d values, %d rounds: total %lld, checksum %lld\n", COUNT, N, ROUNDS, total, check);
    free(all);
    return 0;
}
