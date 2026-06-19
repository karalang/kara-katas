// LeetCode #39 bench mirror — C, the mutable-path backtracking solver (★).
//
// Mirrors bench/combination_sum.kara: an index-bounded DFS with one mutable `path`
// (push/pop on a growable int64 buffer), snapshotting the path into a growable result of
// {data,len} combinations at each target-hit leaf — the C analog of `Vec[Vec[i64]]` +
// `path.clone()`. Same workload (TOTAL enumerations, candidates [2,3,5,7], target = 18 +
// k%13) and the same position-weighted checksum as every other mirror.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Growable int64 buffer (the path, and each stored combination).
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
        size_t ncap = v->cap ? v->cap * 2 : 4;
        v->data = (int64_t *)realloc(v->data, ncap * sizeof(int64_t));
        v->cap = ncap;
    }
    v->data[v->len++] = x;
}

static void vec_pop(Vec *v) { v->len--; }

// Growable list of combinations (snapshots).
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

// Append a deep copy of `src` (the leaf snapshot).
static void vecvec_push_clone(VecVec *vv, const Vec *src) {
    if (vv->len == vv->cap) {
        size_t ncap = vv->cap ? vv->cap * 2 : 8;
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

static void backtrack(const int64_t *candidates, size_t n, size_t start,
                      int64_t remaining, Vec *path, VecVec *out) {
    if (remaining == 0) {
        vecvec_push_clone(out, path);
        return;
    }
    for (size_t i = start; i < n; i++) {
        int64_t c = candidates[i];
        if (c <= remaining) {
            vec_push(path, c);
            backtrack(candidates, n, i, remaining - c, path, out);
            vec_pop(path);
        }
    }
}

int main(void) {
    const int64_t total = 30000;
    const int64_t modulus = 1000000007;
    const int64_t candidates[4] = {2, 3, 5, 7};

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t target = 18 + (k % 13);

        VecVec out;
        vecvec_init(&out);
        Vec path;
        vec_init(&path);
        backtrack(candidates, 4, 0, target, &path, &out);
        free(path.data);

        int64_t sig = 0;
        for (size_t j = 0; j < out.len; j++) {
            const Vec *combo = &out.items[j];
            int64_t s = 0;
            for (size_t i = 0; i < combo->len; i++) {
                s += combo->data[i] * ((int64_t)i + 1);
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
