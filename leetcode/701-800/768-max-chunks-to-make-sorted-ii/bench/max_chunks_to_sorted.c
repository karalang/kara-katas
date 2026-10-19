// LeetCode 768 — Max Chunks To Make Sorted II: benchmark, the ★ arm in C.
// Sixty-four random arrays of 2,000 values, built once; 40,000 rounds
// each count the next one's chunks.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define N 2000

static int64_t seed = 768;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t max_chunks_to_sorted(const int64_t *arr, int64_t n) {
    int64_t *maxima = malloc(n * sizeof(int64_t));
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = arr[i];
        if (top > 0 && x < maxima[top - 1]) {
            int64_t largest = maxima[top - 1];
            while (top > 0 && maxima[top - 1] > x) top--;
            maxima[top++] = largest;
        } else {
            maxima[top++] = x;
        }
    }
    free(maxima);
    return top;
}

int main(void) {
    int64_t rounds = 40000;
    static int64_t pool[64][N];
    for (int p = 0; p < 64; p++) {
        int64_t noise = 1 + next_random() % 40;
        for (int64_t i = 0; i < N; i++) pool[p][i] = i * 50 + next_random() % noise * 50;
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t chunks = max_chunks_to_sorted(pool[round % 64], N);
        total += chunks;
        check = (check * 31 + chunks) % 1000000007;
    }
    printf("%lld arrays of 2000 values: %lld chunks in all, checksum %lld\n",
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
