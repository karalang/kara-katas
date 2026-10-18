// LeetCode #706 bench: the ★ arm in C. See the .kara twin for the
// workload.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BUCKETS 1009

typedef struct {
    int64_t key;
    int64_t value;
} Pair;

typedef struct {
    Pair *pairs;
    int64_t len;
    int64_t cap;
} Bucket;

typedef struct {
    Bucket buckets[BUCKETS];
} MyHashMap;

static void put(MyHashMap *m, int64_t key, int64_t value) {
    Bucket *b = &m->buckets[key % BUCKETS];
    for (int64_t i = 0; i < b->len; i++) {
        if (b->pairs[i].key == key) {
            b->pairs[i].value = value;
            return;
        }
    }
    if (b->len == b->cap) {
        b->cap = b->cap ? 2 * b->cap : 4;
        b->pairs = realloc(b->pairs, sizeof(Pair) * (size_t)b->cap);
    }
    b->pairs[b->len++] = (Pair){key, value};
}

static int64_t get(const MyHashMap *m, int64_t key) {
    const Bucket *b = &m->buckets[key % BUCKETS];
    for (int64_t i = 0; i < b->len; i++) {
        if (b->pairs[i].key == key) {
            return b->pairs[i].value;
        }
    }
    return -1;
}

static void remove_key(MyHashMap *m, int64_t key) {
    Bucket *b = &m->buckets[key % BUCKETS];
    for (int64_t i = 0; i < b->len; i++) {
        if (b->pairs[i].key == key) {
            b->pairs[i] = b->pairs[b->len - 1];
            b->len -= 1;
            return;
        }
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 706;
    int64_t found = 0;
    int64_t checksum = 0;
    for (int round = 0; round < 5; round++) {
        for (int map_no = 0; map_no < 10; map_no++) {
            MyHashMap *map = calloc(1, sizeof(MyHashMap));
            for (int i = 0; i < 300000; i++) {
                int64_t op = next_random(&seed) % 3;
                int64_t hi = next_random(&seed);
                int64_t lo = next_random(&seed);
                int64_t key = (hi * 32768 + lo) % 50000;
                if (op == 0) {
                    int64_t vhi = next_random(&seed);
                    int64_t vlo = next_random(&seed);
                    put(map, key, (vhi * 32768 + vlo) % 1000000);
                } else if (op == 1) {
                    int64_t value = get(map, key);
                    if (value >= 0) {
                        found += 1;
                    }
                    checksum = (checksum * 31 + value + 1) % 1000000007;
                } else {
                    remove_key(map, key);
                }
            }
            for (int b = 0; b < BUCKETS; b++) {
                free(map->buckets[b].pairs);
            }
            free(map);
        }
    }
    printf("5 rounds of 10 maps of 300000 calls: %lld found, checksum %lld\n",
           (long long)found, (long long)checksum);
    return 0;
}
