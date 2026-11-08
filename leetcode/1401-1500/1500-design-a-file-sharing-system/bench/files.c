// LeetCode #1500: Design a File Sharing System -- the benchmark, the same
// structure as files.kara: each chunk's owners in a sorted array kept by
// binary search, each user's chunks in an array indexed by id, free ids in
// a min-heap.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t *a; int64_t len, cap; } Vec;

static void vpush(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->a = realloc(v->a, v->cap * sizeof(int64_t));
    }
    v->a[v->len++] = x;
}

static void vinsert(Vec *v, int64_t at, int64_t x) {
    vpush(v, 0);
    memmove(v->a + at + 1, v->a + at, (v->len - 1 - at) * sizeof(int64_t));
    v->a[at] = x;
}

static void vremove(Vec *v, int64_t at) {
    memmove(v->a + at, v->a + at + 1, (v->len - 1 - at) * sizeof(int64_t));
    v->len--;
}

static int64_t position(const Vec *v, int64_t x) {
    int64_t lo = 0, hi = v->len;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (v->a[mid] < x) lo = mid + 1; else hi = mid;
    }
    return lo;
}

typedef struct {
    Vec *owners;
    int64_t m;
    Vec *owned;
    int64_t users, users_cap;
    Vec heap;
} FileSharing;

static void heap_push(Vec *h, int64_t x) {
    vpush(h, x);
    int64_t i = h->len - 1;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (h->a[p] <= h->a[i]) break;
        int64_t t = h->a[p]; h->a[p] = h->a[i]; h->a[i] = t;
        i = p;
    }
}

static int64_t heap_pop(Vec *h) {
    int64_t top = h->a[0];
    h->a[0] = h->a[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, s = i;
        if (l < h->len && h->a[l] < h->a[s]) s = l;
        if (r < h->len && h->a[r] < h->a[s]) s = r;
        if (s == i) break;
        int64_t t = h->a[s]; h->a[s] = h->a[i]; h->a[i] = t;
        i = s;
    }
    return top;
}

static void fs_new(FileSharing *f, int64_t m) {
    f->m = m;
    f->owners = calloc(m + 1, sizeof(Vec));
    f->users_cap = 16;
    f->owned = calloc(f->users_cap, sizeof(Vec));
    f->users = 1;
    memset(&f->heap, 0, sizeof(Vec));
}

static void fs_free(FileSharing *f) {
    for (int64_t i = 0; i <= f->m; i++) free(f->owners[i].a);
    for (int64_t i = 0; i < f->users; i++) free(f->owned[i].a);
    free(f->owners); free(f->owned); free(f->heap.a);
}

static int64_t fs_join(FileSharing *f, Vec chunks) {
    int64_t id;
    if (f->heap.len > 0) {
        id = heap_pop(&f->heap);
    } else {
        if (f->users == f->users_cap) {
            f->owned = realloc(f->owned, 2 * f->users_cap * sizeof(Vec));
            memset(f->owned + f->users_cap, 0, f->users_cap * sizeof(Vec));
            f->users_cap *= 2;
        }
        id = f->users++;
    }
    for (int64_t i = 0; i < chunks.len; i++) {
        Vec *o = &f->owners[chunks.a[i]];
        vinsert(o, position(o, id), id);
    }
    free(f->owned[id].a);
    f->owned[id] = chunks;
    return id;
}

static void fs_leave(FileSharing *f, int64_t id) {
    Vec *mine = &f->owned[id];
    for (int64_t i = 0; i < mine->len; i++) {
        Vec *o = &f->owners[mine->a[i]];
        vremove(o, position(o, id));
    }
    mine->len = 0;
    heap_push(&f->heap, id);
}

static Vec fs_request(FileSharing *f, int64_t id, int64_t chunk) {
    Vec *o = &f->owners[chunk];
    Vec answer = {0, 0, 0};
    if (o->len > 0) {
        answer.a = malloc(o->len * sizeof(int64_t));
        memcpy(answer.a, o->a, o->len * sizeof(int64_t));
        answer.len = answer.cap = o->len;
        int64_t at = position(o, id);
        if (at == o->len || o->a[at] != id) {
            vinsert(o, at, id);
            vpush(&f->owned[id], chunk);
        }
    }
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static Vec random_chunks(int64_t m, int64_t most, int64_t *seed) {
    int64_t count = next_random(seed) % ((most < m ? most : m) + 1);
    Vec chunks = {0, 0, 0};
    while (chunks.len < count) {
        int64_t c = next_random(seed) % m + 1, seen = 0;
        for (int64_t i = 0; i < chunks.len; i++) if (chunks.a[i] == c) seen = 1;
        if (!seen) vpush(&chunks, c);
    }
    return chunks;
}

static void simulate(int64_t m, int64_t ops, int64_t most, int64_t *seed, int64_t out[4]) {
    FileSharing f;
    fs_new(&f, m);
    Vec live = {0, 0, 0};
    int64_t joins = 0, requests = 0, owners = 0, check = 0;
    for (int64_t k = 0; k < ops; k++) {
        int64_t r = next_random(seed) % 10;
        if (live.len == 0 || r < 3) {
            int64_t id = fs_join(&f, random_chunks(m, most, seed));
            vpush(&live, id);
            joins++;
            check = mix(check, id);
        } else if (r < 5) {
            int64_t at = next_random(seed) % live.len;
            int64_t id = live.a[at];
            live.a[at] = live.a[--live.len];
            fs_leave(&f, id);
        } else {
            int64_t user = live.a[next_random(seed) % live.len];
            int64_t chunk = next_random(seed) % m + 1;
            Vec answer = fs_request(&f, user, chunk);
            requests++;
            owners += answer.len;
            check = mix(check, answer.len);
            for (int64_t i = 0; i < answer.len; i++) check = mix(check, answer.a[i]);
            free(answer.a);
        }
    }
    free(live.a);
    fs_free(&f);
    out[0] = joins; out[1] = requests; out[2] = owners; out[3] = check;
}

static void batch(int64_t count, int64_t most_m, int64_t ops, int64_t most, int64_t *seed) {
    int64_t joins = 0, requests = 0, owners = 0, check = 0, o[4];
    for (int64_t i = 0; i < count; i++) {
        int64_t m = next_random(seed) % most_m + 1;
        simulate(m, ops, most, seed, o);
        joins += o[0]; requests += o[1]; owners += o[2];
        check = mix(check, o[3]);
    }
    printf("%lld systems of up to %lld chunks, %lld calls each: %lld joins, %lld requests, %lld owners returned, checksum %lld\n",
           (long long)count, (long long)most_m, (long long)ops, (long long)joins, (long long)requests,
           (long long)owners, (long long)check);
}

int main(void) {
    int64_t seed = 1500;
    batch(40, 2000, 40000, 30, &seed);
    return 0;
}
