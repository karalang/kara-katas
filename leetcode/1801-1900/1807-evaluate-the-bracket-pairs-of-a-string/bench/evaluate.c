// LeetCode #1807: Evaluate the Bracket Pairs of a String -- the bench in C:
// the ★ arm over 40 strings of 10^5 characters and 40 knowledge lists of
// 2 * 10^4 pairs built once, 200 calls. The map is an open-addressed table
// of copied keys and values, hashed by FNV-1a.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 65536
#define PAIRS 20000
#define MOST 100000

typedef struct {
    char *key, *value;
    size_t key_len, value_len;
} Entry;

typedef struct {
    char key[11], value[11];
    size_t key_len, value_len;
} Pair;

static uint64_t fnv(const char *text, size_t len) {
    uint64_t h = 1469598103934665603ULL;
    for (size_t i = 0; i < len; i++) h = (h ^ (unsigned char)text[i]) * 1099511628211ULL;
    return h;
}

static char *copy(const char *text, size_t len) {
    char *c = malloc(len + 1);
    memcpy(c, text, len);
    return c;
}

// the result goes to `out`, whose length is returned
static size_t evaluate(const char *s, size_t n, const Pair *knowledge, size_t k, char *out) {
    static Entry table[SLOTS];
    memset(table, 0, sizeof table);
    for (size_t p = 0; p < k; p++) {
        size_t slot = fnv(knowledge[p].key, knowledge[p].key_len) & (SLOTS - 1);
        while (table[slot].key) slot = (slot + 1) & (SLOTS - 1);
        table[slot].key = copy(knowledge[p].key, knowledge[p].key_len);
        table[slot].key_len = knowledge[p].key_len;
        table[slot].value = copy(knowledge[p].value, knowledge[p].value_len);
        table[slot].value_len = knowledge[p].value_len;
    }
    size_t len = 0;
    char key[MOST];
    size_t key_len = 0;
    int inside = 0;
    for (size_t i = 0; i < n; i++) {
        char c = s[i];
        if (c == '(') {
            inside = 1;
        } else if (c == ')') {
            size_t slot = fnv(key, key_len) & (SLOTS - 1);
            Entry *found = NULL;
            while (table[slot].key) {
                if (table[slot].key_len == key_len && memcmp(table[slot].key, key, key_len) == 0) {
                    found = &table[slot];
                    break;
                }
                slot = (slot + 1) & (SLOTS - 1);
            }
            if (found) {
                memcpy(out + len, found->value, found->value_len);
                len += found->value_len;
            } else {
                out[len++] = '?';
            }
            key_len = 0;
            inside = 0;
        } else if (inside) {
            key[key_len++] = c;
        } else {
            out[len++] = c;
        }
    }
    for (size_t slot = 0; slot < SLOTS; slot++) {
        free(table[slot].key);
        free(table[slot].value);
    }
    return len;
}

static int64_t seed = 1807;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static size_t word(char *w, int64_t most, int64_t letters) {
    size_t n = (size_t)(1 + next_random() % most);
    for (size_t i = 0; i < n; i++) w[i] = (char)(97 + next_random() % letters);
    return n;
}

// a set of the keys drawn so far, to keep the knowledge's keys distinct
static int insert_seen(char (*seen)[11], size_t *seen_len, const char *k, size_t len) {
    size_t slot = fnv(k, len) & (SLOTS - 1);
    while (seen_len[slot]) {
        if (seen_len[slot] == len && memcmp(seen[slot], k, len) == 0) return 0;
        slot = (slot + 1) & (SLOTS - 1);
    }
    memcpy(seen[slot], k, len);
    seen_len[slot] = len;
    return 1;
}

int main(void) {
    static char texts[40][MOST];
    static size_t text_len[40];
    static Pair lists[40][PAIRS];
    static char seen[SLOTS][11];
    static size_t seen_len[SLOTS];
    static char out[20 * MOST];
    for (int t = 0; t < 40; t++) {
        size_t len = 0;
        while (len < 99980) {
            if (next_random() % 2 == 0) {
                len += word(texts[t] + len, 3, 26);
            } else {
                texts[t][len++] = '(';
                len += word(texts[t] + len, 8, 4);
                texts[t][len++] = ')';
            }
        }
        text_len[t] = len;
        memset(seen_len, 0, sizeof seen_len);
        size_t k = 0;
        while (k < PAIRS) {
            char w[11];
            size_t wl = word(w, 8, 4);
            if (insert_seen(seen, seen_len, w, wl)) {
                memcpy(lists[t][k].key, w, wl);
                lists[t][k].key_len = wl;
                lists[t][k].value_len = word(lists[t][k].value, 10, 26);
                k++;
            }
        }
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 200; call++) {
        int64_t t = (check + call) % 40;
        int64_t l = (check * 7 + call) % 40;
        size_t len = evaluate(texts[t], text_len[t], lists[l], PAIRS, out);
        check = (check * 31 + (int64_t)len + (unsigned char)out[len / 2]) % 1000000007;
    }
    printf("200 calls over 40 strings of 10^5 characters: checksum %lld\n", (long long)check);
    return 0;
}
