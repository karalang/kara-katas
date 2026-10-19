// LeetCode 769 — Max Chunks To Make Sorted: benchmark, the ★ arm in C.
// Sixty-four near-sorted permutations of 2,000, built once; 150,000
// rounds each count the next one's chunks.
#include <stdio.h>
#include <stdint.h>

#define N 2000

static int64_t seed = 769;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t max_chunks_to_sorted(const int64_t *arr, int64_t n) {
    int64_t chunks = 0, largest = 0;
    for (int64_t i = 0; i < n; i++) {
        if (arr[i] > largest) largest = arr[i];
        if (largest == i) chunks++;
    }
    return chunks;
}

int main(void) {
    int64_t rounds = 150000;
    static int64_t pool[64][N];
    for (int p = 0; p < 64; p++) {
        for (int64_t i = 0; i < N; i++) pool[p][i] = i;
        int64_t swaps = next_random() % N;
        for (int64_t s = 0; s < swaps; s++) {
            int64_t i = next_random() % N;
            int64_t j = i + 1 + next_random() % 4;
            if (j > N - 1) j = N - 1;
            int64_t t = pool[p][i];
            pool[p][i] = pool[p][j];
            pool[p][j] = t;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t chunks = max_chunks_to_sorted(pool[round % 64], N);
        total += chunks;
        check = (check * 31 + chunks) % 1000000007;
    }
    printf("%lld permutations of 2000: %lld chunks in all, checksum %lld\n",
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
