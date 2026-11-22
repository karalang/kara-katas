// LeetCode #2736: Maximum Sum Queries -- the bench (queries.kara in C):
// pairs and queries by nums1 and x falling, sorted by qsort, a stack of
// (nums2, sum) with nums2 rising and sums falling, and a binary search
// per query.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t a, b; } Pair;
typedef struct { int64_t x, y, index; } Query;

static int by_first_falling(const void *p, const void *q) {
    int64_t x = ((const Pair *)p)->a, y = ((const Pair *)q)->a;
    return (x < y) - (x > y);
}

static int by_x_falling(const void *p, const void *q) {
    int64_t x = ((const Query *)p)->x, y = ((const Query *)q)->x;
    return (x < y) - (x > y);
}

static void maximum_sum_queries(const int64_t *nums1, const int64_t *nums2, int64_t n, const int64_t *qx,
                                const int64_t *qy, int64_t q, int64_t *answer) {
    Pair *pairs = malloc(sizeof(Pair) * n);
    for (int64_t i = 0; i < n; i++) pairs[i] = (Pair){nums1[i], nums2[i]};
    qsort(pairs, (size_t)n, sizeof(Pair), by_first_falling);
    Query *order = malloc(sizeof(Query) * q);
    for (int64_t i = 0; i < q; i++) order[i] = (Query){qx[i], qy[i], i};
    qsort(order, (size_t)q, sizeof(Query), by_x_falling);
    Pair *stack = malloc(sizeof(Pair) * n);
    int64_t top = 0, j = 0;
    for (int64_t k = 0; k < q; k++) {
        int64_t x = order[k].x, y = order[k].y;
        while (j < n && pairs[j].a >= x) {
            int64_t a = pairs[j].a, b = pairs[j].b;
            j++;
            if (top > 0 && stack[top - 1].a >= b) continue;
            while (top > 0 && stack[top - 1].b <= a + b) top--;
            stack[top++] = (Pair){b, a + b};
        }
        int64_t low = 0, high = top;
        while (low < high) {
            int64_t middle = (low + high) / 2;
            if (stack[middle].a >= y) high = middle;
            else low = middle + 1;
        }
        answer[order[k].index] = low < top ? stack[low].b : -1;
    }
    free(pairs); free(order); free(stack);
}

static int64_t seed = 2736;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t random_up_to(int64_t most) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % most + 1;
}

int main(void) {
    const int cases = 10, rounds = 3;
    const int64_t n = 100000;
    int64_t *nums1 = malloc(sizeof(int64_t) * n * cases), *nums2 = malloc(sizeof(int64_t) * n * cases);
    int64_t *qx = malloc(sizeof(int64_t) * n * cases), *qy = malloc(sizeof(int64_t) * n * cases);
    for (int c = 0; c < cases; c++) {
        for (int64_t i = 0; i < n; i++) nums1[c * n + i] = random_up_to(1000000000);
        for (int64_t i = 0; i < n; i++) nums2[c * n + i] = random_up_to(1000000000);
        for (int64_t i = 0; i < n; i++) {
            qx[c * n + i] = random_up_to(1000000000);
            qy[c * n + i] = random_up_to(1000000000);
        }
    }
    int64_t *answer = malloc(sizeof(int64_t) * n);
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < cases; c++) {
            maximum_sum_queries(nums1 + c * n, nums2 + c * n, n, qx + c * n, qy + c * n, n, answer);
            for (int64_t i = 0; i < n; i++) {
                sum += answer[i];
                check = (check * 31 + answer[i] + 1 + r) % 1000000007;
            }
        }
    }
    printf("%d cases of %lld pairs and queries, %d rounds: answers sum to %lld, checksum %lld\n", cases, (long long)n, rounds, (long long)sum, (long long)check);
    free(nums1); free(nums2); free(qx); free(qy); free(answer);
    return 0;
}
