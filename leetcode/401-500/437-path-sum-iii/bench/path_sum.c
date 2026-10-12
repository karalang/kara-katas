// Benchmark for #437: mirror of path_sum.kara (prefix sums along the
// path) on one random tree of 100,000 nodes, queried for 200 targets.
// The nodes live in one array, linked by index; the prefix counts are an
// open-addressing table of 64-bit keys, cleared for each target.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS (1 << 18)

typedef struct { int64_t val, left, right; } Node;
typedef struct { int64_t key, count; int used; } Slot;

static Node *nodes;
static Slot *table;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static Slot *slot_for(int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    size_t i = (size_t)(h >> 46);
    while (table[i].used && table[i].key != key) {
        i = (i + 1) & (SLOTS - 1);
    }
    return &table[i];
}

static int64_t count_from(int64_t node, int64_t prefix, int64_t target) {
    if (node < 0) {
        return 0;
    }
    int64_t sum = prefix + nodes[node].val;
    Slot *s = slot_for(sum - target);
    int64_t found = s->used ? s->count : 0;
    s = slot_for(sum);
    s->used = 1;
    s->key = sum;
    s->count++;
    found += count_from(nodes[node].left, sum, target);
    found += count_from(nodes[node].right, sum, target);
    slot_for(sum)->count--;
    return found;
}

static int64_t path_sum(int64_t root, int64_t target) {
    memset(table, 0, SLOTS * sizeof(Slot));
    Slot *s = slot_for(0);
    s->used = 1;
    s->key = 0;
    s->count = 1;
    return count_from(root, 0, target);
}

int main(void) {
    const int64_t size = 100000, queries = 200;
    int64_t seed = 437;
    nodes = malloc(size * sizeof(Node));
    table = malloc(SLOTS * sizeof(Slot));
    int64_t *open = malloc(size * sizeof(int64_t));
    // Each node hangs under a random earlier node that still has a free
    // side, values in [-1000, 1000].
    nodes[0] = (Node){next_random(&seed) % 2001 - 1000, -1, -1};
    int64_t open_len = 1;
    open[0] = 0;
    for (int64_t id = 1; id < size; id++) {
        int64_t at = next_random(&seed) % open_len;
        int64_t parent = open[at];
        nodes[id] = (Node){next_random(&seed) % 2001 - 1000, -1, -1};
        if (nodes[parent].left < 0 && (nodes[parent].right >= 0 || next_random(&seed) % 2 == 0)) {
            nodes[parent].left = id;
        } else {
            nodes[parent].right = id;
        }
        if (nodes[parent].left >= 0 && nodes[parent].right >= 0) {
            open[at] = open[open_len - 1];
            open_len--;
        }
        open[open_len++] = id;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t target = next_random(&seed) % 4001 - 2000;
        int64_t count = path_sum(0, target);
        total += count;
        checksum = (checksum * 31 + count) % 1000000007;
    }
    printf("%lld targets on a tree of %lld: %lld paths, checksum %lld\n",
           (long long)queries, (long long)size, (long long)total, (long long)checksum);
    free(open);
    free(table);
    free(nodes);
    return 0;
}
