// Benchmark for #841: Keys and Rooms -- the ★ arm (a stack of rooms to open).
//
// Mirrors keys_and_rooms.kara: room 0 is open; every room opened is put
// on a stack, and a room taken off the stack gives up its keys, each key
// to a room not yet opened opening it. As in the Kāra program, each room
// keeps its keys in its own growable array, and every count allocates
// its marks and its stack.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, (size_t)v->cap * sizeof *v->data);
    }
    v->data[v->len++] = x;
}

static bool contains(const Vec *v, int64_t x) {
    for (int64_t i = 0; i < v->len; i++)
        if (v->data[i] == x) return true;
    return false;
}

static bool can_visit_all_rooms(const Vec *rooms, int64_t n) {
    bool *opened = calloc((size_t)n, sizeof *opened);
    opened[0] = true;
    int64_t count = 1;
    Vec stack = {0, 0, 0};
    push(&stack, 0);
    while (stack.len > 0) {
        int64_t room = stack.data[--stack.len];
        for (int64_t k = 0; k < rooms[room].len; k++) {
            int64_t key = rooms[room].data[k];
            if (!opened[key]) {
                opened[key] = true;
                count += 1;
                push(&stack, key);
            }
        }
    }
    free(stack.data);
    free(opened);
    return count == n;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 64 cases drawn once, each LeetCode's most rooms, 1000: case g puts
    // 2000 keys, each to a random room, in random rooms, no room holding
    // two keys to the same room; when g is even it then threads the
    // rooms in a shuffled order, each holding a key to the next, so that
    // every room can be visited. Each round asks the next case.
    enum { COUNT = 64, N = 1000 };
    const int64_t rounds = 36000, n = N;
    int64_t seed = 841;
    static Vec cases[COUNT][N];
    static int64_t order[N];
    for (int64_t g = 0; g < COUNT; g++) {
        Vec *rooms = cases[g];
        for (int64_t k = 0; k < 2000; k++) {
            int64_t from = next_random(&seed) % n;
            int64_t to = next_random(&seed) % n;
            if (!contains(&rooms[from], to)) push(&rooms[from], to);
        }
        if (g % 2 == 0) {
            for (int64_t i = 0; i < n; i++) order[i] = i;
            for (int64_t i = n - 1; i >= 2; i--) {
                int64_t j = 1 + next_random(&seed) % i;
                int64_t t = order[i];
                order[i] = order[j];
                order[j] = t;
            }
            for (int64_t i = 0; i < n - 1; i++)
                if (!contains(&rooms[order[i]], order[i + 1])) push(&rooms[order[i]], order[i + 1]);
        }
    }
    int64_t yes = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        bool all = can_visit_all_rooms(cases[round % COUNT], n);
        if (all) yes += 1;
        checksum = (checksum * 31 + (all ? round % 1000 : 7)) % 1000000007;
    }
    printf("%lld rounds of %d cases: %lld with every room visited, checksum %lld\n", (long long)rounds, COUNT,
           (long long)yes, (long long)checksum);
    return 0;
}
