// LeetCode #1057: Campus Bikes -- the benchmark, mirror of campus_bikes.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t w, b; } Pair;
typedef struct { Pair *items; int64_t len, cap; } Bucket;

static void push(Bucket *v, Pair p) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->items = realloc(v->items, (size_t)v->cap * sizeof(Pair));
    }
    v->items[v->len++] = p;
}

static int64_t abs64(int64_t x) { return x < 0 ? -x : x; }

static int64_t *assign_bikes(const int64_t (*workers)[2], int64_t n, const int64_t (*bikes)[2], int64_t m) {
    Bucket *buckets = calloc(2000, sizeof(Bucket));
    for (int64_t w = 0; w < n; w++) {
        for (int64_t b = 0; b < m; b++) {
            int64_t d = abs64(workers[w][0] - bikes[b][0]) + abs64(workers[w][1] - bikes[b][1]);
            push(&buckets[d], (Pair){w, b});
        }
    }
    int64_t *bike_of = malloc((size_t)n * sizeof(int64_t));
    for (int64_t w = 0; w < n; w++) bike_of[w] = -1;
    bool *taken = calloc((size_t)m, sizeof(bool));
    int64_t left = n;
    for (int64_t d = 0; d < 2000; d++) {
        Bucket *bucket = &buckets[d];
        for (int64_t k = 0; k < bucket->len; k++) {
            int64_t w = bucket->items[k].w, b = bucket->items[k].b;
            if (left > 0 && bike_of[w] < 0 && !taken[b]) {
                bike_of[w] = b;
                taken[b] = true;
                left -= 1;
            }
        }
        free(bucket->items);
    }
    free(buckets);
    free(taken);
    return bike_of;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t (*random_places(int64_t count, int64_t *seed))[2] {
    int64_t (*places)[2] = malloc((size_t)count * sizeof *places);
    for (int64_t i = 0; i < count; i++) {
        int64_t x = next_random(seed) % 1000;
        int64_t y = next_random(seed) % 1000;
        places[i][0] = x;
        places[i][1] = y;
    }
    return places;
}

int main(void) {
    enum { COUNT = 20, ROUNDS = 8, WORKERS = 300, BIKES = 400 };
    int64_t seed = 1057;
    int64_t (*workers[COUNT])[2];
    int64_t (*bikes[COUNT])[2];
    for (int c = 0; c < COUNT; c++) {
        workers[c] = random_places(WORKERS, &seed);
        bikes[c] = random_places(BIKES, &seed);
    }
    int64_t ridden = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t *answer = assign_bikes((const int64_t (*)[2])workers[c], WORKERS, (const int64_t (*)[2])bikes[c], BIKES);
            for (int64_t w = 0; w < WORKERS; w++) {
                int64_t b = answer[w];
                ridden += abs64(workers[c][w][0] - bikes[c][b][0]) + abs64(workers[c][w][1] - bikes[c][b][1]);
                check = (check * 131 + b + 1) % 1000000007;
            }
            free(answer);
        }
    }
    printf("%d campuses of %d workers and %d bikes, %d rounds: %lld ridden, checksum %lld\n", COUNT, WORKERS, BIKES, ROUNDS, (long long)ridden, (long long)check);
    return 0;
}
