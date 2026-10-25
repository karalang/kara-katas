// Benchmark: LeetCode #996 Number of Squareful Arrays -- the ★ arm,
// backtracking over the sorted values, on random arrays of 12 values,
// LeetCode's largest. Mirrors num_squareful_perms.kara, .rs, .py and
// go-seq/.
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool is_square(int64_t s) {
    int64_t r = (int64_t)sqrt((double)s);
    while (r * r > s) r--;
    while ((r + 1) * (r + 1) <= s) r++;
    return r * r == s;
}

static int64_t place(const int64_t *a, bool *used, int64_t n, int64_t depth, int64_t last) {
    if (depth == n) return 1;
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (used[i]) continue;
        if (i > 0 && a[i] == a[i - 1] && !used[i - 1]) continue;
        if (depth > 0 && !is_square(last + a[i])) continue;
        used[i] = true;
        count += place(a, used, n, depth + 1, a[i]);
        used[i] = false;
    }
    return count;
}

static int cmp_i64(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int64_t num_squareful_perms(const int64_t *nums, int64_t n) {
    int64_t *a = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t i = 0; i < n; i++) a[i] = nums[i];
    qsort(a, (size_t)n, sizeof(int64_t), cmp_i64);
    bool *used = calloc((size_t)n, sizeof(bool));
    int64_t count = place(a, used, n, 0, 0);
    free(used);
    free(a);
    return count;
}

static int64_t seed = 996;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// 12 values below 50, each making a square with the one before
static void random_walk(int64_t *nums) {
    nums[0] = next_random() % 50;
    for (int k = 1; k < 12; k++) {
        int64_t v = nums[k - 1], options[16], m = 0;
        for (int64_t r = 0; r * r < v + 50; r++) {
            if (r * r >= v) options[m++] = r * r - v;
        }
        nums[k] = options[next_random() % m];
    }
}

int main(void) {
    int rounds = 300;
    int64_t arrays[20][12];
    for (int i = 0; i < 20; i++) random_walk(arrays[i]);
    int64_t found = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int64_t got = num_squareful_perms(arrays[(r + i) % 20], 12);
            found += got;
            check = (check * 31 + got + 1) % 1000000007;
        }
    }
    printf("%d rounds over 20 arrays of 12 values: %lld squareful permutations, checksum %lld\n", rounds,
           (long long)found, (long long)check);
    return 0;
}
