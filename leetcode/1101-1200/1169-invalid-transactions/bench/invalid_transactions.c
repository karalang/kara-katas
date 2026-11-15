// LeetCode #1169: Invalid Transactions -- the ★ arm's bench in C: each
// transaction split into its fields, the places of each name's
// transactions gathered in an open-addressing hash table (FNV-1a), and
// every transaction compared with the others of its name.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[16], city[16];
    int64_t time, amount;
} Txn;

typedef struct {
    const char *name;  // NULL when the slot is empty
    int64_t *at;
    int64_t n, cap;
} Slot;

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static void parse(const char *t, Txn *x) {
    const char *p = t;
    size_t k = strcspn(p, ",");
    memcpy(x->name, p, k);
    x->name[k] = 0;
    p += k + 1;
    x->time = strtoll(p, (char **)&p, 10);
    x->amount = strtoll(p + 1, (char **)&p, 10);
    strcpy(x->city, p + 1);
}

// The invalid transactions of `ts`, as pointers into it, in order; their
// count in *nout.
static const char **invalid_transactions(char *const *ts, int64_t n, int64_t *nout) {
    Txn *txns = malloc(n * sizeof(Txn));
    int64_t cap = 1;
    while (cap < 2 * n) cap <<= 1;
    Slot *table = calloc(cap, sizeof(Slot));
    int64_t *slot_of = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        parse(ts[i], &txns[i]);
        uint64_t s = fnv(txns[i].name) & (cap - 1);
        while (table[s].name && strcmp(table[s].name, txns[i].name) != 0) s = (s + 1) & (cap - 1);
        Slot *e = &table[s];
        if (!e->name) e->name = txns[i].name;
        if (e->n == e->cap) {
            e->cap = e->cap ? 2 * e->cap : 4;
            e->at = realloc(e->at, e->cap * sizeof(int64_t));
        }
        e->at[e->n++] = i;
        slot_of[i] = s;
    }
    const char **out = malloc(n * sizeof(char *));
    int64_t k = 0;
    for (int64_t i = 0; i < n; i++) {
        const Txn *t = &txns[i];
        int bad = t->amount > 1000;
        const Slot *e = &table[slot_of[i]];
        for (int64_t q = 0; !bad && q < e->n; q++) {
            const Txn *o = &txns[e->at[q]];
            int64_t d = o->time - t->time;
            if (d < 0) d = -d;
            if (d <= 60 && strcmp(o->city, t->city) != 0) bad = 1;
        }
        if (bad) out[k++] = ts[i];
    }
    for (int64_t s = 0; s < cap; s++) free(table[s].at);
    free(table);
    free(slot_of);
    free(txns);
    *nout = k;
    return out;
}

static int64_t seed = 1169;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *line(void) {
    int64_t name = next_random() % 200;
    int64_t time = next_random() % 1001;
    int64_t amount = next_random() % 1101;
    int64_t city = next_random() % 2;
    char buf[64];
    int len = snprintf(buf, sizeof buf, "n%lld,%lld,%lld,c%lld", (long long)name, (long long)time,
                       (long long)amount, (long long)city);
    char *s = malloc(len + 1);
    memcpy(s, buf, len + 1);
    return s;
}

int main(void) {
    static char *lists[16][1000];
    for (int k = 0; k < 16; k++)
        for (int i = 0; i < 1000; i++) lists[k][i] = line();
    int64_t total = 0, check = 0;
    for (int r = 0; r < 300; r++) {
        for (int k = 0; k < 16; k++) {
            int64_t at = next_random() % 1000;
            free(lists[k][at]);
            lists[k][at] = line();
            int64_t nb;
            const char **bad = invalid_transactions(lists[k], 1000, &nb);
            total += nb;
            for (int64_t b = 0; b < nb; b++) check = (check * 31 + (int64_t)strlen(bad[b])) % 1000000007;
            free(bad);
        }
    }
    printf("300 rounds over 16 lists of 1000 transactions: %lld invalid, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
