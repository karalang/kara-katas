// LeetCode #705 bench: the ★ arm in C. See the .kara twin for the
// workload.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BUCKETS 1009

typedef struct {
    int64_t *keys;
    int64_t len;
    int64_t cap;
} Bucket;

typedef struct {
    Bucket buckets[BUCKETS];
} MyHashSet;

static bool bucket_has(const Bucket *b, int64_t key) {
    for (int64_t i = 0; i < b->len; i++) {
        if (b->keys[i] == key) {
            return true;
        }
    }
    return false;
}

static void add(MyHashSet *s, int64_t key) {
    Bucket *b = &s->buckets[key % BUCKETS];
    if (!bucket_has(b, key)) {
        if (b->len == b->cap) {
            b->cap = b->cap ? 2 * b->cap : 4;
            b->keys = realloc(b->keys, sizeof(int64_t) * (size_t)b->cap);
        }
        b->keys[b->len++] = key;
    }
}

static void remove_key(MyHashSet *s, int64_t key) {
    Bucket *b = &s->buckets[key % BUCKETS];
    for (int64_t i = 0; i < b->len; i++) {
        if (b->keys[i] == key) {
            b->keys[i] = b->keys[b->len - 1];
            b->len -= 1;
            return;
        }
    }
}

static bool contains(const MyHashSet *s, int64_t key) {
    return bucket_has(&s->buckets[key % BUCKETS], key);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 705;
    int64_t found = 0;
    int64_t checksum = 0;
    for (int round = 0; round < 5; round++) {
        for (int set_no = 0; set_no < 10; set_no++) {
            MyHashSet *set = calloc(1, sizeof(MyHashSet));
            for (int i = 0; i < 300000; i++) {
                int64_t op = next_random(&seed) % 3;
                int64_t hi = next_random(&seed);
                int64_t lo = next_random(&seed);
                int64_t key = (hi * 32768 + lo) % 50000;
                if (op == 0) {
                    add(set, key);
                } else if (op == 1) {
                    remove_key(set, key);
                } else {
                    bool yes = contains(set, key);
                    if (yes) {
                        found += 1;
                    }
                    checksum = (checksum * 3 + (yes ? 1 : 2)) % 1000000007;
                }
            }
            for (int b = 0; b < BUCKETS; b++) {
                free(set->buckets[b].keys);
            }
            free(set);
        }
    }
    printf("5 rounds of 10 sets of 300000 calls: %lld found, checksum %lld\n",
           (long long)found, (long long)checksum);
    return 0;
}
