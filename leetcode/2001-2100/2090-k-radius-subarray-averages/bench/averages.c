// LeetCode #2090: K Radius Subarray Averages -- C mirror of the ★ arm's
// benchmark (averages.kara): the same 30 arrays, each asked for the same 10
// radii, one slide of the window into a fresh `malloc`'d buffer each.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t seed = 2090;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t *get_averages(const int64_t *nums, int64_t n, int64_t k) {
    int64_t width = 2 * k + 1;
    int64_t *avgs = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) avgs[i] = -1;
    int64_t sum = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += nums[i];
        if (i >= width) sum -= nums[i - width];
        if (i + 1 >= width) avgs[i - k] = sum / width;
    }
    return avgs;
}

int main(void) {
    int64_t *arrays = malloc((size_t)30 * N * sizeof(int64_t));
    for (int t = 0; t < 30; t++)
        for (int i = 0; i < N; i++) arrays[(size_t)t * N + i] = next_random() % 100001;
    static const int64_t radii[10] = {0, 1, 3, 10, 30, 100, 300, 1000, 3000, 20000};
    int64_t total = 0, check = 0;
    for (int t = 0; t < 30; t++) {
        for (int r = 0; r < 10; r++) {
            int64_t *avgs = get_averages(arrays + (size_t)t * N, N, radii[r]);
            int64_t s = 0;
            for (int i = 0; i < N; i++) s += avgs[i];
            free(avgs);
            total += s;
            check = (check * 31 + s) % 1000000007;
        }
    }
    printf("300 answers: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(arrays);
    return 0;
}
