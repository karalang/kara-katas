// LeetCode #2093: Minimum Cost to Reach City With Discounts -- C mirror of
// the ★ arm's benchmark (discounts.kara): the same 60 maps, each asked by
// the same Dijkstra over (city, used) states with a binary heap in a
// `malloc`'d array, ordered as the tuples are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

typedef struct { int64_t cost, city, used; } Item;
typedef struct { int64_t other, toll; } Road;
typedef struct { Road *v; int64_t len, cap; } Roads;

static Item *heap;
static int64_t heap_len, heap_cap;

static int less(const Item *x, const Item *y) {
    if (x->cost != y->cost) return x->cost < y->cost;
    if (x->city != y->city) return x->city < y->city;
    return x->used < y->used;
}

static void push(Item it) {
    if (heap_len == heap_cap) {
        heap_cap = heap_cap ? heap_cap * 2 : 64;
        heap = realloc(heap, heap_cap * sizeof(Item));
    }
    int64_t i = heap_len++;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!less(&it, &heap[p])) break;
        heap[i] = heap[p];
        i = p;
    }
    heap[i] = it;
}

static Item pop(void) {
    Item top = heap[0];
    Item last = heap[--heap_len];
    int64_t i = 0;
    for (;;) {
        int64_t c = 2 * i + 1;
        if (c >= heap_len) break;
        if (c + 1 < heap_len && less(&heap[c + 1], &heap[c])) c++;
        if (!less(&heap[c], &last)) break;
        heap[i] = heap[c];
        i = c;
    }
    heap[i] = last;
    return top;
}

static void road_push(Roads *r, int64_t other, int64_t toll) {
    if (r->len == r->cap) {
        r->cap = r->cap ? r->cap * 2 : 4;
        r->v = realloc(r->v, r->cap * sizeof(Road));
    }
    r->v[r->len++] = (Road){other, toll};
}

static int64_t minimum_cost(int64_t n, const int64_t (*highways)[3], int64_t m, int64_t discounts) {
    Roads *roads = calloc(n, sizeof(Roads));
    for (int64_t i = 0; i < m; i++) {
        road_push(&roads[highways[i][0]], highways[i][1], highways[i][2]);
        road_push(&roads[highways[i][1]], highways[i][0], highways[i][2]);
    }
    int64_t k = discounts + 1;
    int64_t *best = malloc(n * k * sizeof(int64_t));
    for (int64_t i = 0; i < n * k; i++) best[i] = INT64_MAX;
    heap_len = 0;
    best[0] = 0;
    push((Item){0, 0, 0});
    int64_t answer = -1;
    while (heap_len > 0) {
        Item it = pop();
        int64_t cost = it.cost, city = it.city, used = it.used;
        if (city == n - 1) {
            answer = cost;
            break;
        }
        if (cost > best[city * k + used]) continue;
        for (int64_t j = 0; j < roads[city].len; j++) {
            int64_t other = roads[city].v[j].other, toll = roads[city].v[j].toll;
            int64_t full = cost + toll;
            if (full < best[other * k + used]) {
                best[other * k + used] = full;
                push((Item){full, other, used});
            }
            if (used < discounts) {
                int64_t half = cost + toll / 2;
                if (half < best[other * k + used + 1]) {
                    best[other * k + used + 1] = half;
                    push((Item){half, other, used + 1});
                }
            }
        }
    }
    for (int64_t i = 0; i < n; i++) free(roads[i].v);
    free(roads);
    free(best);
    return answer;
}

int main(void) {
    int64_t seed = 2093;
    int64_t n = 20000;
    int64_t total = 0, check = 0;
    int64_t (*highways)[3] = malloc(3 * n * sizeof *highways);
    const int64_t bases[3] = {1, 1667, 3333};
    for (int64_t g = 0; g < 60; g++) {
        int64_t m = 0;
        for (int64_t a = 0; a < n; a++) {
            for (int j = 0; j < 3; j++) {
                int64_t b = (a + bases[j] + next_random(&seed) % 1666) % n;
                int64_t hi = next_random(&seed);
                int64_t toll = (hi * 32768 + next_random(&seed)) % 100001;
                highways[m][0] = a;
                highways[m][1] = b;
                highways[m][2] = toll;
                m++;
            }
        }
        int64_t c = minimum_cost(n, (const int64_t (*)[3])highways, m, g % 12 * 2);
        total += c;
        check = (check * 31 + c + 2) % 1000000007;
    }
    printf("60 answers: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(highways);
    free(heap);
    return 0;
}
