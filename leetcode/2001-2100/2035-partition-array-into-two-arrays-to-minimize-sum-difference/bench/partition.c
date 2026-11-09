// LeetCode #2035: Partition Array Into Two Arrays to Minimize Sum
// Difference -- the ★ arm in C, the same algorithm and workload as
// partition.kara: each half's subset sums listed by size, the right lists
// sorted, and for each left sum a lower bound on the right sums that bring
// the side to half the total, with the sums on either side of it tried.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 15

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

// sums[size] holds count[size] sums, room for C(N, size) each
static void subset_sums(const int64_t *half, int64_t **sums, int64_t *count) {
    for (int s = 0; s <= N; s++) count[s] = 0;
    for (int64_t mask = 0; mask < (1 << N); mask++) {
        int64_t sum = 0, size = 0;
        for (int i = 0; i < N; i++) {
            if (mask >> i & 1) {
                sum += half[i];
                size++;
            }
        }
        sums[size][count[size]++] = sum;
    }
}

static int64_t *left[N + 1], *right[N + 1];
static int64_t lcount[N + 1], rcount[N + 1];

static int64_t minimum_difference(const int64_t *nums) {
    int64_t total = 0;
    for (int i = 0; i < 2 * N; i++) total += nums[i];
    subset_sums(nums, left, lcount);
    subset_sums(nums + N, right, rcount);
    for (int s = 0; s <= N; s++) qsort(right[s], rcount[s], sizeof(int64_t), cmp);
    int64_t best = INT64_MAX;
    for (int k = 0; k <= N; k++) {
        const int64_t *others = right[N - k];
        int64_t m = rcount[N - k];
        for (int64_t i = 0; i < lcount[k]; i++) {
            int64_t a = left[k][i];
            int64_t lo = 0, hi = m;
            while (lo < hi) {
                int64_t mid = lo + (hi - lo) / 2;
                if (2 * (a + others[mid]) < total) lo = mid + 1;
                else hi = mid;
            }
            if (lo < m) {
                int64_t d = total - 2 * (a + others[lo]);
                d = d < 0 ? -d : d;
                if (d < best) best = d;
            }
            if (lo > 0) {
                int64_t d = total - 2 * (a + others[lo - 1]);
                d = d < 0 ? -d : d;
                if (d < best) best = d;
            }
        }
    }
    return best;
}

static int64_t seed = 2035;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t choose = 1;
    for (int s = 0; s <= N; s++) {
        left[s] = malloc(choose * sizeof(int64_t));
        right[s] = malloc(choose * sizeof(int64_t));
        choose = choose * (N - s) / (s + 1);
    }
    static int64_t arrays[40][2 * N];
    static const int64_t tops[5] = {10000000, 1000, 100, 10000000, 50};
    for (int a = 0; a < 40; a++) {
        int64_t top = tops[a % 5];
        for (int i = 0; i < 2 * N; i++) {
            int64_t hi = next_random();
            int64_t lo = next_random();
            arrays[a][i] = (hi * 32768 + lo) % (2 * top + 1) - top;
        }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t round = 0; round < 5; round++) {
        for (int64_t a = 0; a < 40; a++) {
            int64_t at = (round * 7 + a * 3) % 30;
            arrays[a][at] = -arrays[a][at];
            int64_t answer = minimum_difference(arrays[a]);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007LL;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
