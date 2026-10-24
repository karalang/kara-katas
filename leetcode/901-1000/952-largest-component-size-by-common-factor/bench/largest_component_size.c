// LeetCode #952 bench: C mirror of largest_component_size.kara (the ★
// arm, union by prime) on the same 20 sets. C has no hash map, so the
// first place of each prime is an open-addressing table with linear
// probing.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys;
    int64_t *vals;
    size_t mask;
} Index;

static size_t slot(int64_t key, size_t mask) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    return (size_t)(h >> 32) & mask;
}

static void index_init(Index *ix, size_t n) {
    size_t cap = 1;
    while (cap < 2 * n) cap <<= 1;
    ix->keys = malloc(cap * sizeof(int64_t));
    ix->vals = malloc(cap * sizeof(int64_t));
    ix->mask = cap - 1;
    for (size_t i = 0; i < cap; i++) ix->keys[i] = -1;
}

// The slot holding key, or the empty slot where it would go.
static size_t index_find(const Index *ix, int64_t key) {
    size_t s = slot(key, ix->mask);
    while (ix->keys[s] != -1 && ix->keys[s] != key) s = (s + 1) & ix->mask;
    return s;
}

static int64_t find(int64_t *parent, int64_t x) {
    int64_t root = x;
    while (parent[root] != root) root = parent[root];
    int64_t y = x;
    while (parent[y] != root) {
        int64_t next = parent[y];
        parent[y] = root;
        y = next;
    }
    return root;
}

static int64_t largest_component_size(const int64_t *nums, int64_t n) {
    int64_t *parent = malloc((size_t)n * sizeof(int64_t));
    int64_t *size = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        parent[i] = i;
        size[i] = 1;
    }
    // a number up to 100000 has at most 6 distinct primes
    Index first;
    index_init(&first, (size_t)n * 6);
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        int64_t p = 2;
        while (x > 1) {
            if (p * p > x) p = x;
            if (x % p == 0) {
                while (x % p == 0) x /= p;
                size_t s = index_find(&first, p);
                if (first.keys[s] == p) {
                    int64_t a = find(parent, i);
                    int64_t b = find(parent, first.vals[s]);
                    if (a != b) {
                        if (size[a] < size[b]) {
                            parent[a] = b;
                            size[b] += size[a];
                        } else {
                            parent[b] = a;
                            size[a] += size[b];
                        }
                    }
                } else {
                    first.keys[s] = p;
                    first.vals[s] = i;
                }
            }
            p += 1;
        }
    }
    int64_t best = 0;
    for (int64_t i = 0; i < n; i++) {
        if (parent[i] == i && size[i] > best) best = size[i];
    }
    free(parent);
    free(size);
    free(first.keys);
    free(first.vals);
    return best;
}

static int64_t seed = 952;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 40, count = 20, n = 2000;
    // 20 sets of 2000 distinct numbers from 1 to 100000
    static int64_t sets[20][2000];
    char *taken = malloc(100001);
    for (int64_t c = 0; c < count; c++) {
        for (int v = 0; v <= 100000; v++) taken[v] = 0;
        int64_t len = 0;
        while (len < n) {
            int64_t hi = next_random();
            int64_t v = 1 + (hi * 32768 + next_random()) % 100000;
            if (!taken[v]) {
                taken[v] = 1;
                sets[c][len++] = v;
            }
        }
    }
    free(taken);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t k = (r + i) % count;
            int64_t size = largest_component_size(sets[k], n);
            total += size;
            check = (check * 31 + size) % 1000000007;
        }
    }
    printf("%lld rounds over %lld sets of %lld numbers up to 100000: largest components adding to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)total, (long long)check);
    return 0;
}
