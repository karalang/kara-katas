// LeetCode #2233: Maximum Product After K Increments -- the benchmark's
// C mirror of product.kara: the smallest raised k times through a binary
// min-heap, then the heap emptied into the product.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *heap;
static int64_t size;

static void push(int64_t x) {
    int64_t i = size++;
    heap[i] = x;
    while (i > 0) {
        int64_t parent = (i - 1) / 2;
        if (heap[parent] <= heap[i]) break;
        int64_t t = heap[parent]; heap[parent] = heap[i]; heap[i] = t;
        i = parent;
    }
}

static int64_t pop(void) {
    int64_t top = heap[0];
    heap[0] = heap[--size];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < size && heap[l] < heap[m]) m = l;
        if (r < size && heap[r] < heap[m]) m = r;
        if (m == i) break;
        int64_t t = heap[m]; heap[m] = heap[i]; heap[i] = t;
        i = m;
    }
    return top;
}

static int64_t maximum_product(const int64_t *nums, int64_t n, int64_t k) {
    size = 0;
    for (int64_t i = 0; i < n; i++) push(nums[i]);
    for (int64_t j = 0; j < k; j++) {
        int64_t smallest = pop();
        push(smallest + 1);
    }
    int64_t product = 1;
    while (size > 0) product = product * pop() % 1000000007;
    return product;
}

static int64_t seed = 2233;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t n = 20000;
    int64_t *nums = malloc(n * sizeof *nums);
    heap = malloc(n * sizeof *heap);
    for (int64_t i = 0; i < n; i++) nums[i] = wide_random() % 1000001;
    int64_t check = 0;
    for (int pass = 0; pass < 150; pass++) {
        // punch: one number drawn again before each pass
        int64_t at = next_random() % 20000;
        nums[at] = wide_random() % 1000001;
        check = (check * 31 + maximum_product(nums, n, 50000)) % 1000000007;
    }
    printf("150 passes over 20000 numbers, k = 50000: checksum %lld\n", (long long)check);
    free(nums);
    free(heap);
    return 0;
}
