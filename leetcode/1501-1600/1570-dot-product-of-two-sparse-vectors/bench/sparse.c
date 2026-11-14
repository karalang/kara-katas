// LeetCode #1570: Dot Product of Two Sparse Vectors -- bench: the ★ arm
// (index-ordered pairs merged by two pointers) over 20 vectors of 500000
// values, one in 10 of them from 1 to 100 and the rest 0, each made sparse
// once; then the product of every ordered pair of them, 400 products.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t index, value;
} Pair;

typedef struct {
    Pair *pairs;
    int64_t len;
} SparseVector;

static SparseVector sparse_new(const int64_t *nums, int64_t n) {
    SparseVector v = {NULL, 0};
    int64_t cap = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] != 0) {
            if (v.len == cap) {
                cap = cap ? cap * 2 : 4;
                v.pairs = realloc(v.pairs, sizeof(Pair) * cap);
            }
            v.pairs[v.len++] = (Pair){i, nums[i]};
        }
    }
    return v;
}

static int64_t dot_product(const SparseVector *a, const SparseVector *b) {
    int64_t i = 0, j = 0, total = 0;
    while (i < a->len && j < b->len) {
        int64_t x = a->pairs[i].index, y = b->pairs[j].index;
        if (x == y) {
            total += a->pairs[i].value * b->pairs[j].value;
            i++;
            j++;
        } else if (x < y) {
            i++;
        } else {
            j++;
        }
    }
    return total;
}

static int64_t seed = 1570;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const int64_t n = 500000;
    SparseVector vectors[20];
    int64_t *nums = malloc(sizeof(int64_t) * n);
    for (int v = 0; v < 20; v++) {
        for (int64_t i = 0; i < n; i++) {
            int64_t draw = next_random();
            nums[i] = draw % 10 == 0 ? draw / 10 % 100 + 1 : 0;
        }
        vectors[v] = sparse_new(nums, n);
    }
    free(nums);
    int64_t check = 0, total = 0;
    for (int i = 0; i < 20; i++) {
        for (int j = 0; j < 20; j++) {
            int64_t product = dot_product(&vectors[i], &vectors[j]);
            total += product;
            check = mix(check, product);
        }
    }
    printf("400 products of 20 vectors of 500000 values: products sum %lld, checksum %lld\n", (long long)total,
           (long long)check);
    for (int v = 0; v < 20; v++) free(vectors[v].pairs);
    return 0;
}
