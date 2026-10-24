// Benchmark: LeetCode #981 Time Based Key-Value Store -- the ★ arm, a
// list per key and binary search, on LeetCode's largest sessions of
// 200,000 calls. Mirrors time_map.kara, .rs, .py and go-seq/.
//
// The map is an open-addressing hash table on the key's FNV-1a hash.
// A set copies its value; a key is copied the first time it is set. A
// get returns the stored value without copying it.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t timestamp;
    char *value;
} Entry;

typedef struct {
    char *key;
    Entry *list;
    size_t len, cap;
} Slot;

typedef struct {
    Slot *slots;
    size_t cap, used;
} TimeMap;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) {
        h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    }
    return h;
}

static Slot *find(Slot *slots, size_t cap, const char *key) {
    size_t i = hash(key) & (cap - 1);
    while (slots[i].key && strcmp(slots[i].key, key) != 0) {
        i = (i + 1) & (cap - 1);
    }
    return &slots[i];
}

static void tm_init(TimeMap *tm) {
    tm->cap = 16;
    tm->used = 0;
    tm->slots = calloc(tm->cap, sizeof(Slot));
}

static void tm_grow(TimeMap *tm) {
    size_t cap = tm->cap * 2;
    Slot *slots = calloc(cap, sizeof(Slot));
    for (size_t i = 0; i < tm->cap; i++) {
        if (tm->slots[i].key) {
            *find(slots, cap, tm->slots[i].key) = tm->slots[i];
        }
    }
    free(tm->slots);
    tm->slots = slots;
    tm->cap = cap;
}

static void tm_set(TimeMap *tm, const char *key, const char *value, int64_t timestamp) {
    if ((tm->used + 1) * 8 > tm->cap * 7) {
        tm_grow(tm);
    }
    Slot *s = find(tm->slots, tm->cap, key);
    if (!s->key) {
        s->key = strdup(key);
        tm->used++;
    }
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 4;
        s->list = realloc(s->list, s->cap * sizeof(Entry));
    }
    s->list[s->len].timestamp = timestamp;
    s->list[s->len].value = strdup(value);
    s->len++;
}

static const char *tm_get(const TimeMap *tm, const char *key, int64_t timestamp) {
    Slot *s = find(tm->slots, tm->cap, key);
    if (!s->key) {
        return "";
    }
    size_t lo = 0, hi = s->len;
    while (lo < hi) {
        size_t mid = (lo + hi) / 2;
        if (s->list[mid].timestamp <= timestamp) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo == 0 ? "" : s->list[lo - 1].value;
}

static void tm_free(TimeMap *tm) {
    for (size_t i = 0; i < tm->cap; i++) {
        Slot *s = &tm->slots[i];
        if (s->key) {
            for (size_t j = 0; j < s->len; j++) {
                free(s->list[j].value);
            }
            free(s->list);
            free(s->key);
        }
    }
    free(tm->slots);
}

static int64_t seed = 981;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 20;
    int calls = 200000;
    char keys[1000][16];
    char values[100][16];
    for (int64_t i = 0; i < 1000; i++) {
        snprintf(keys[i], sizeof keys[i], "user%lld", (long long)(i * 7919 % 100000));
    }
    for (int64_t i = 0; i < 100; i++) {
        snprintf(values[i], sizeof values[i], "value%lld", (long long)(i * 104729 % 1000000));
    }
    long long found = 0;
    int64_t check = 0;
    for (int r = 0; r < rounds; r++) {
        TimeMap tm;
        tm_init(&tm);
        int64_t now = 0;
        for (int c = 0; c < calls; c++) {
            int64_t k = next_random() % 1000;
            if (next_random() % 2 == 0) {
                now += 1 + next_random() % 3;
                tm_set(&tm, keys[k], values[next_random() % 100], now);
            } else {
                int64_t t = 1 + next_random() % (now + 3);
                const char *got = tm_get(&tm, keys[k], t);
                size_t len = strlen(got);
                if (len > 0) {
                    found++;
                }
                check = (check * 131 + (int64_t)len) % 1000000007;
                for (size_t i = 0; i < len; i++) {
                    check = (check * 131 + (unsigned char)got[i]) % 1000000007;
                }
            }
        }
        tm_free(&tm);
    }
    printf("%d rounds of %d calls on 1000 keys: %lld values found, checksum %lld\n", rounds, calls, found,
           (long long)check);
    return 0;
}
