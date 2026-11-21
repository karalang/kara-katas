// LeetCode #1743: Restore the Array From Adjacent Pairs -- the bench
// (restore.kara in C): the pairs as a graph, walked from an end. The
// neighbour lists go in an open-addressing hash table written for the
// bench, rebuilt for each restore; a value has at most two neighbours.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS (1 << 18)
#define EMPTY INT32_MIN

typedef struct {
    int32_t key;
    int32_t count;
    int32_t near[2];
} Slot;

static Slot *table;

static uint32_t slot_of(int32_t key) {
    uint32_t i = ((uint32_t)key * 2654435761u) >> 14;
    while (table[i].key != EMPTY && table[i].key != key) i = (i + 1) & (SLOTS - 1);
    return i;
}

static void add(int32_t a, int32_t b) {
    Slot *s = &table[slot_of(a)];
    s->key = a;
    s->near[s->count++] = b;
}

// `order` has room for n values
static void restore_array(const int32_t (*pairs)[2], int64_t m, int32_t *order) {
    for (int64_t i = 0; i < SLOTS; i++) table[i].key = EMPTY, table[i].count = 0;
    for (int64_t i = 0; i < m; i++) {
        add(pairs[i][0], pairs[i][1]);
        add(pairs[i][1], pairs[i][0]);
    }
    int64_t i = 0;
    while (table[i].key == EMPTY || table[i].count != 1) i++;
    order[0] = table[i].key;
    order[1] = table[i].near[0];
    for (int64_t k = 2; k < m + 1; k++) {
        const Slot *s = &table[slot_of(order[k - 1])];
        order[k] = s->near[0] == order[k - 2] ? s->near[1] : s->near[0];
    }
}

static int64_t seed = 1743;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

enum { COUNT = 10, ROUNDS = 4, N = 100000 };

int main(void) {
    table = malloc(sizeof(Slot) * SLOTS);
    static int32_t pairs[COUNT][N - 1][2];
    static int32_t values[N];
    static unsigned char taken[200001];
    for (int c = 0; c < COUNT; c++) {
        memset(taken, 0, sizeof taken);
        int64_t have = 0;
        while (have < N) {
            int64_t v = wide() % 200001 - 100000;
            if (!taken[v + 100000]) {
                taken[v + 100000] = 1;
                values[have++] = (int32_t)v;
            }
        }
        for (int64_t i = 1; i < N; i++) {
            if (next_random() % 2 == 0) {
                pairs[c][i - 1][0] = values[i - 1];
                pairs[c][i - 1][1] = values[i];
            } else {
                pairs[c][i - 1][0] = values[i];
                pairs[c][i - 1][1] = values[i - 1];
            }
        }
        for (int64_t i = N - 2; i >= 1; i--) {
            int64_t j = wide() % (i + 1);
            int32_t a = pairs[c][i][0], b = pairs[c][i][1];
            pairs[c][i][0] = pairs[c][j][0];
            pairs[c][i][1] = pairs[c][j][1];
            pairs[c][j][0] = a;
            pairs[c][j][1] = b;
        }
    }
    static int32_t order[N];
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            restore_array(pairs[c], N - 1, order);
            int32_t first = order[0], last = order[N - 1];
            int32_t middle = first < last ? order[N / 2] : order[N - 1 - N / 2];
            int64_t low = first < last ? first : last;
            sum += low;
            check = (check * 31 + low + middle + 200000 + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: smaller ends sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)sum, (long long)check);
    free(table);
    return 0;
}
