// LeetCode #2250: Count Number of Rectangles Containing Each Point -- the
// benchmark's C mirror of rectangles.kara: rectangles bucketed by height,
// each bucket's lengths sorted, a point summing over the buckets of height
// y to 100 how many lengths are at least x (a lower-bound binary search).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 50000

static int64_t rect_len[N], rect_h[N], pt_x[N], pt_y[N], counts[N];
static int64_t bucket[101][N];
static int bucket_n[101];

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static void count_rectangles(int r, int p) {
    for (int h = 0; h <= 100; h++) bucket_n[h] = 0;
    for (int i = 0; i < r; i++) bucket[rect_h[i]][bucket_n[rect_h[i]]++] = rect_len[i];
    for (int h = 0; h <= 100; h++) qsort(bucket[h], bucket_n[h], sizeof(int64_t), cmp_i64);
    for (int i = 0; i < p; i++) {
        int64_t count = 0;
        for (int64_t h = pt_y[i]; h < 101; h++) {
            int lo = 0, hi = bucket_n[h];
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                if (bucket[h][mid] < pt_x[i]) lo = mid + 1; else hi = mid;
            }
            count += bucket_n[h] - lo;
        }
        counts[i] = count;
    }
}

static int64_t seed = 2250;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 4; t++) {
        for (int i = 0; i < N; i++) {
            rect_len[i] = wide_random() % 1000000000 + 1;
            rect_h[i] = next_random() % 100 + 1;
        }
        for (int i = 0; i < N; i++) {
            pt_x[i] = wide_random() % 1000000000 + 1;
            pt_y[i] = next_random() % 100 + 1;
        }
        count_rectangles(N, N);
        for (int i = 0; i < N; i++) check = (check * 31 + counts[i]) % 1000000007;
    }
    printf("4 cases of 5 * 10^4 rectangles and points: checksum %lld\n", (long long)check);
    return 0;
}
