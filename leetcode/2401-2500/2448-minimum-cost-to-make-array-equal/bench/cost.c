// LeetCode #2448: Minimum Cost to Make Array Equal -- the bench, the ★
// arm: the pairs sorted, the weighted median the first value whose
// running cost reaches half the total, and every value moved there.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t value, cost;
} Pair;

static int by_pair(const void *a, const void *b) {
    const Pair *x = a, *y = b;
    if (x->value != y->value) return x->value < y->value ? -1 : 1;
    if (x->cost != y->cost) return x->cost < y->cost ? -1 : 1;
    return 0;
}

static int64_t min_cost(const int64_t *nums, const int64_t *cost, int64_t n) {
    Pair *pairs = malloc(n * sizeof(Pair));
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        pairs[i].value = nums[i];
        pairs[i].cost = cost[i];
        total += cost[i];
    }
    qsort(pairs, n, sizeof(Pair), by_pair);
    int64_t running = 0, target = 0;
    for (int64_t i = 0; i < n; i++) {
        running += pairs[i].cost;
        if (2 * running >= total) {
            target = pairs[i].value;
            break;
        }
    }
    free(pairs);
    int64_t answer = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t d = nums[i] - target;
        answer += (d < 0 ? -d : d) * cost[i];
    }
    return answer;
}

static int64_t seed = 2448;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int64_t *nums = malloc(n * sizeof(int64_t));
    int64_t *cost = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t r = next_random();
        nums[i] = 1 + (r * 32768 + next_random()) % 1000000;
        r = next_random();
        cost[i] = 1 + (r * 32768 + next_random()) % 1000000;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 200; p++) {
        for (int64_t t = 0; t < 1000; t++) cost[(1000 * p + t) % n] = 1 + next_random() * 30;
        check = (check * 31 + min_cost(nums, cost, n) % 1000000007 + p) % 1000000007;
    }
    printf("200 passes over 10^5 values: checksum %lld\n", (long long)check);
    free(nums);
    free(cost);
    return 0;
}
