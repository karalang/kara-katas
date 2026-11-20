// LeetCode #1675: Minimize Deviation in Array -- the bench's C mirror: the
// ★ arm on 50 arrays of 50000 values up to 10^9, all drawn first, each
// answered 10 times. C has no priority queue; a binary max-heap is written
// for the bench.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define ARRAYS 50
#define N 50000
#define ROUNDS 10

static void heap_push(int32_t *heap, int64_t *len, int32_t v) {
    int64_t i = (*len)++;
    while (i > 0) {
        int64_t parent = (i - 1) / 2;
        if (heap[parent] >= v) break;
        heap[i] = heap[parent];
        i = parent;
    }
    heap[i] = v;
}

static int32_t heap_pop(int32_t *heap, int64_t *len) {
    int32_t top = heap[0];
    int32_t last = heap[--(*len)];
    int64_t i = 0;
    for (;;) {
        int64_t child = 2 * i + 1;
        if (child >= *len) break;
        if (child + 1 < *len && heap[child + 1] > heap[child]) child++;
        if (heap[child] <= last) break;
        heap[i] = heap[child];
        i = child;
    }
    if (*len > 0) heap[i] = last;
    return top;
}

static int32_t minimum_deviation(const int32_t *nums, int64_t n) {
    int32_t *heap = malloc((size_t)n * sizeof *heap);
    int64_t len = 0;
    int32_t smallest = INT32_MAX;
    for (int64_t i = 0; i < n; i++) {
        int32_t start = nums[i] % 2 == 1 ? nums[i] * 2 : nums[i];
        heap_push(heap, &len, start);
        if (start < smallest) smallest = start;
    }
    int32_t best = INT32_MAX;
    for (;;) {
        int32_t top = heap_pop(heap, &len);
        if (top - smallest < best) best = top - smallest;
        if (top % 2 == 1) break;
        if (top / 2 < smallest) smallest = top / 2;
        heap_push(heap, &len, top / 2);
    }
    free(heap);
    return best;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1675;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t nums[ARRAYS][N];
    for (int a = 0; a < ARRAYS; a++) {
        for (int i = 0; i < N; i++) nums[a][i] = (int32_t)((next_random() * 32768 + next_random()) % 1000000000 + 1);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int a = 0; a < ARRAYS; a++) {
            int32_t deviation = minimum_deviation(nums[a], N);
            total += deviation;
            check = (check * 31 + deviation + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: deviations sum to %lld, checksum %lld\n", ARRAYS, N, ROUNDS, (long long)total, (long long)check);
    return 0;
}
