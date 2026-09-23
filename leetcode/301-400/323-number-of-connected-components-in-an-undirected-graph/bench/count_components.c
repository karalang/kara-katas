// Benchmark mirror of LeetCode #323 — same disjoint-set forest as
// bench/count_components.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define NODES 1000000
#define PASSES 16
#define STRIDE 9973
#define MODULUS 1073741789

static int64_t *parent, *size_, sets;

static void reset(void) {
    for (int64_t i = 0; i < NODES; i++) {
        parent[i] = i;
        size_[i] = 1;
    }
    sets = NODES;
}

static int64_t find(int64_t x) {
    int64_t root = x;
    while (parent[root] != root) root = parent[root];
    int64_t cur = x;
    while (parent[cur] != root) {
        int64_t next = parent[cur];
        parent[cur] = root;
        cur = next;
    }
    return root;
}

static void merge(int64_t a, int64_t b) {
    int64_t ra = find(a), rb = find(b);
    if (ra == rb) return;
    if (size_[ra] < size_[rb]) {
        int64_t t = ra;
        ra = rb;
        rb = t;
    }
    parent[rb] = ra;
    size_[ra] += size_[rb];
    sets -= 1;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t draw(int64_t *seed, int64_t bound) {
    int64_t hi = next(seed);
    int64_t lo = next(seed);
    return (hi * 32768 + lo) % bound;
}

int main(void) {
    int64_t seed = 323, sink = 0;
    parent = malloc(NODES * sizeof(int64_t));
    size_ = malloc(NODES * sizeof(int64_t));
    for (int64_t p = 0; p < PASSES; p++) {
        reset();
        int64_t m = (1 + p % 4) * NODES / 4;
        for (int64_t e = 0; e < m; e++) {
            int64_t a = draw(&seed, NODES);
            int64_t b = draw(&seed, NODES);
            merge(a, b);
        }
        int64_t probe = 0;
        for (int64_t i = 0; i < NODES; i += STRIDE) probe = (probe * 31 + find(i)) % MODULUS;
        sink = (sink * 131 + sets + probe) % MODULUS;
    }
    printf("sink %lld components %lld\n", (long long)sink, (long long)sets);
    free(parent);
    free(size_);
    return 0;
}
