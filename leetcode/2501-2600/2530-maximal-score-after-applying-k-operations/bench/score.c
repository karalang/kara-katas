// LeetCode #2530: Maximal Score After Applying K Operations -- C mirror of
// the benchmark (score.kara): the same numbers, passes, order and
// checksum, with a binary max-heap in an array.
#include <stdint.h>
#include <stdio.h>

#define N 100000

static int64_t nums[N], heap[N];
static int64_t size;

static void push(int64_t x) {
    int64_t i = size++;
    heap[i] = x;
    while (i > 0) {
        int64_t parent = (i - 1) / 2;
        if (heap[parent] >= heap[i]) break;
        int64_t t = heap[parent]; heap[parent] = heap[i]; heap[i] = t;
        i = parent;
    }
}

static int64_t pop(void) {
    int64_t top = heap[0];
    heap[0] = heap[--size];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, big = i;
        if (l < size && heap[l] > heap[big]) big = l;
        if (r < size && heap[r] > heap[big]) big = r;
        if (big == i) break;
        int64_t t = heap[big]; heap[big] = heap[i]; heap[i] = t;
        i = big;
    }
    return top;
}

static int64_t max_kelements(int64_t k) {
    size = 0;
    for (int i = 0; i < N; i++) push(nums[i]);
    int64_t score = 0;
    for (int64_t s = 0; s < k; s++) {
        int64_t top = pop();
        score += top;
        push((top + 2) / 3);
    }
    return score;
}

static int64_t seed = 2530;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    for (int i = 0; i < N; i++) nums[i] = wide_random() % 1000000000 + 1;
    const int passes = 170;
    int64_t check = 0;
    for (int p = 0; p < passes; p++) {
        int64_t k = 50000 + check % 50001;
        check = (check * 31 + max_kelements(k) % 1000000007 + p) % 1000000007;
    }
    printf("%d passes over 100000 numbers: checksum %lld\n", passes, (long long)check);
    return 0;
}
