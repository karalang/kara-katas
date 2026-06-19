// LeetCode #47 bench mirror — C, the sorted used-array adjacent-skip backtracker (★).
//
// Mirrors bench/permutations_ii.kara: sort a working copy, then a DFS that picks any still-unused
// element (tracked by a `used` byte array) with a same-level adjacent-duplicate skip, snapshotting
// the path into a growable result of {data,len} permutations at each leaf — the C analog of
// Vec[Vec[i64]] + path.clone(). Same workload (TOTAL permutations of a fixed n=8 multiset from
// {1,2,3,4}, one slot punched per iteration) and the same position-weighted checksum as every
// other mirror.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct {
    int64_t *data;
    size_t len;
    size_t cap;
} Vec;

static void vec_init(Vec *v) {
    v->data = NULL;
    v->len = 0;
    v->cap = 0;
}

static void vec_push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 8;
        v->data = (int64_t *)realloc(v->data, ncap * sizeof(int64_t));
        v->cap = ncap;
    }
    v->data[v->len++] = x;
}

static void vec_pop(Vec *v) { v->len--; }

typedef struct {
    Vec *items;
    size_t len;
    size_t cap;
} VecVec;

static void vecvec_init(VecVec *vv) {
    vv->items = NULL;
    vv->len = 0;
    vv->cap = 0;
}

static void vecvec_push_clone(VecVec *vv, const Vec *src) {
    if (vv->len == vv->cap) {
        size_t ncap = vv->cap ? vv->cap * 2 : 16;
        vv->items = (Vec *)realloc(vv->items, ncap * sizeof(Vec));
        vv->cap = ncap;
    }
    Vec snap;
    vec_init(&snap);
    if (src->len) {
        snap.data = (int64_t *)malloc(src->len * sizeof(int64_t));
        memcpy(snap.data, src->data, src->len * sizeof(int64_t));
        snap.len = src->len;
        snap.cap = src->len;
    }
    vv->items[vv->len++] = snap;
}

static void vecvec_free(VecVec *vv) {
    for (size_t i = 0; i < vv->len; i++) free(vv->items[i].data);
    free(vv->items);
}

static void backtrack(const int64_t *nums, size_t n, unsigned char *used,
                      Vec *path, VecVec *out) {
    if (path->len == n) {
        vecvec_push_clone(out, path);
        return;
    }
    for (size_t i = 0; i < n; i++) {
        if (used[i]) continue;
        if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;
        used[i] = 1;
        vec_push(path, nums[i]);
        backtrack(nums, n, used, path, out);
        vec_pop(path);
        used[i] = 0;
    }
}

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    const int64_t total = 600;
    const int64_t modulus = 1000000007;
    const int64_t n = 8;
    int64_t nums[8];
    for (int64_t b = 0; b < n; b++) nums[b] = 1 + (b % 4);

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        nums[k % n] = 1 + (k % 4);

        int64_t work[8];
        memcpy(work, nums, (size_t)n * sizeof(int64_t));
        qsort(work, (size_t)n, sizeof(int64_t), cmp_i64);

        VecVec out;
        vecvec_init(&out);
        Vec path;
        vec_init(&path);
        unsigned char used[8] = {0};
        backtrack(work, (size_t)n, used, &path, &out);
        free(path.data);

        int64_t sig = 0;
        for (size_t j = 0; j < out.len; j++) {
            const Vec *perm = &out.items[j];
            int64_t s = 0;
            for (size_t i = 0; i < perm->len; i++) {
                s += perm->data[i] * ((int64_t)i + 1);
            }
            sig = (sig * 31 + s) % modulus;
        }
        sig = (sig + (int64_t)out.len) % modulus;
        acc = (acc * 131 + sig) % modulus;

        vecvec_free(&out);
    }

    printf("%lld\n", (long long)acc);
    return 0;
}
