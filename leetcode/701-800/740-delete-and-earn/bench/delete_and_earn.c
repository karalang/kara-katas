// LeetCode #740: Delete and Earn -- house robber over values.
// Benchmark mirror of the Kara star arm: total the points each value is
// worth in a table as long as the largest value, then walk the values
// in order keeping the best total with the last value taken and with
// it left. The table is a growable array, as in the Kara arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static int64_t delete_and_earn(const int64_t *nums, int64_t n) {
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++)
        if (nums[i] > top) top = nums[i];
    Vec points = {0, 0, 0};
    for (int64_t v = 0; v < top + 1; v++) push(&points, 0);
    for (int64_t i = 0; i < n; i++) points.data[nums[i]] += nums[i];
    int64_t take = 0, skip = 0;
    for (int64_t v = 0; v < top + 1; v++) {
        int64_t taken = skip + points.data[v];
        skip = take > skip ? take : skip;
        take = taken;
    }
    free(points.data);
    return take > skip ? take : skip;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 740, n = 20000, total = 0;
    int64_t *nums = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) nums[i] = 1 + next_random(&seed) % 10000;
    for (int r = 0; r < 5000; r++) {
        for (int k = 0; k < 20; k++) {
            int64_t j = next_random(&seed) % n;
            nums[j] = 1 + next_random(&seed) % 10000;
        }
        total += delete_and_earn(nums, n);
    }
    printf("5000 rounds of 20000 numbers: %lld points in all\n", (long long)total);
    free(nums);
    return 0;
}
