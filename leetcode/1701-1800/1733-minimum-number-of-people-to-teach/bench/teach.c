// LeetCode #1733: Minimum Number of People to Teach -- the bench
// (teach.kara): the stuck users gathered in a set, and the language most
// of them know.
//
// C has no set: each user's languages go in a table of 32 slots and the
// stuck users in one of 1024, both probed linearly with the key hashed by
// one multiply, which is less work than the SipHash sets of Kāra and Rust
// or Go's map.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 50
#define ROUNDS 200
#define N 500
#define USERS 500
#define PAIRS 500
#define LANG_SLOTS 32
#define USER_SLOTS 1024

static uint32_t slot_of(uint32_t key, uint32_t mask) { return (key * 2654435761u >> 7) & mask; }

// insert `key` (never 0) into `table`; 1 if it was new
static int insert(int32_t *table, uint32_t mask, int32_t key) {
    uint32_t s = slot_of((uint32_t)key, mask);
    while (table[s] != 0) {
        if (table[s] == key) {
            return 0;
        }
        s = (s + 1) & mask;
    }
    table[s] = key;
    return 1;
}

static int contains(const int32_t *table, uint32_t mask, int32_t key) {
    uint32_t s = slot_of((uint32_t)key, mask);
    while (table[s] != 0) {
        if (table[s] == key) {
            return 1;
        }
        s = (s + 1) & mask;
    }
    return 0;
}

static int32_t minimum_teachings(int32_t n, int32_t languages[USERS][11], int32_t friendships[PAIRS][2]) {
    int32_t *known = calloc((size_t)USERS * LANG_SLOTS, sizeof(int32_t));
    for (int u = 0; u < USERS; u++) {
        for (int i = 1; i <= languages[u][0]; i++) {
            insert(known + u * LANG_SLOTS, LANG_SLOTS - 1, languages[u][i]);
        }
    }
    int32_t *stuck = calloc(USER_SLOTS, sizeof(int32_t));
    int32_t stuck_len = 0;
    for (int f = 0; f < PAIRS; f++) {
        int u = friendships[f][0] - 1, v = friendships[f][1] - 1;
        const int32_t *a = known + u * LANG_SLOTS, *b = known + v * LANG_SLOTS;
        int disjoint = 1;
        for (int s = 0; s < LANG_SLOTS && disjoint; s++) {
            if (a[s] != 0 && contains(b, LANG_SLOTS - 1, a[s])) {
                disjoint = 0;
            }
        }
        if (disjoint) {
            stuck_len += insert(stuck, USER_SLOTS - 1, u + 1);
            stuck_len += insert(stuck, USER_SLOTS - 1, v + 1);
        }
    }
    int32_t *speakers = calloc((size_t)n + 1, sizeof(int32_t));
    for (int s = 0; s < USER_SLOTS; s++) {
        if (stuck[s] != 0) {
            const int32_t *k = known + (stuck[s] - 1) * LANG_SLOTS;
            for (int t = 0; t < LANG_SLOTS; t++) {
                if (k[t] != 0) {
                    speakers[k[t]]++;
                }
            }
        }
    }
    int32_t best = 0;
    for (int l = 0; l <= n; l++) {
        if (speakers[l] > best) {
            best = speakers[l];
        }
    }
    free(known);
    free(stuck);
    free(speakers);
    return stuck_len - best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

// each user's count of languages, then the languages
static int32_t languages[COUNT][USERS][11];
static int32_t friendships[COUNT][PAIRS][2];
static uint8_t friends[USERS][USERS];

int main(void) {
    int64_t seed = 1733;
    for (int c = 0; c < COUNT; c++) {
        for (int u = 0; u < USERS; u++) {
            int k = (int)(next_random(&seed) % 10 + 1);
            int32_t *known = languages[c][u];
            known[0] = 0;
            while (known[0] < k) {
                int32_t l = (int32_t)(next_random(&seed) % N + 1);
                int seen = 0;
                for (int i = 1; i <= known[0]; i++) {
                    seen |= known[i] == l;
                }
                if (!seen) {
                    known[++known[0]] = l;
                }
            }
        }
        memset(friends, 0, sizeof friends);
        int made = 0;
        while (made < PAIRS) {
            int u = (int)(next_random(&seed) % USERS);
            int v = (int)(next_random(&seed) % USERS);
            if (u != v && !friends[u][v]) {
                friends[u][v] = friends[v][u] = 1;
                friendships[c][made][0] = u + 1;
                friendships[c][made][1] = v + 1;
                made++;
            }
        }
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = minimum_teachings(N, languages[c], friendships[c]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %d users, %d languages and %d friendships, %d rounds: teachings sum to %lld, checksum %lld\n",
           COUNT, USERS, N, PAIRS, ROUNDS, (long long)sum, (long long)check);
    return 0;
}
