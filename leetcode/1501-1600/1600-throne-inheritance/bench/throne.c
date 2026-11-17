// LeetCode #1600: Throne Inheritance
// -- the bench in C, mirroring throne.kara: C has no map, so each name is
// kept in an open-addressing table hashed by FNV-1a (linear probing,
// grown at half full) whose entry holds the person's children as a
// growable array of names and whether they are dead; the preorder is
// walked with a stack and each name in the order is copied, as Kāra's
// `to_string` does. Through 10 reigns of 50000 calls, drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
    char **kids;
    int nkids, capkids;
    int dead;
} Entry;

typedef struct {
    Entry *slots;
    size_t cap, len;
} Table;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (uint8_t)*s) * 1099511628211ULL;
    return h;
}

static void grow(Table *t) {
    Entry *old = t->slots;
    size_t oldcap = t->cap;
    t->cap = oldcap ? oldcap * 2 : 64;
    t->slots = calloc(t->cap, sizeof(Entry));
    t->len = 0;
    for (size_t i = 0; i < oldcap; i++) {
        if (!old[i].name) continue;
        size_t j = hash(old[i].name) & (t->cap - 1);
        while (t->slots[j].name) j = (j + 1) & (t->cap - 1);
        t->slots[j] = old[i];
        t->len++;
    }
    free(old);
}

// The entry for `name`; with `create`, a fresh one (its name owned by the
// table) when it is missing, else NULL.
static Entry *find(Table *t, const char *name, int create) {
    if (create && (t->len + 1) * 2 > t->cap) grow(t);
    if (!t->cap) return NULL;
    for (size_t i = hash(name) & (t->cap - 1);; i = (i + 1) & (t->cap - 1)) {
        if (!t->slots[i].name) {
            if (!create) return NULL;
            t->slots[i].name = strdup(name);
            t->len++;
            return &t->slots[i];
        }
        if (strcmp(t->slots[i].name, name) == 0) return &t->slots[i];
    }
}

static void table_free(Table *t) {
    for (size_t i = 0; i < t->cap; i++) {
        if (t->slots[i].name) {
            for (int k = 0; k < t->slots[i].nkids; k++) free(t->slots[i].kids[k]);
            free(t->slots[i].kids);
            free(t->slots[i].name);
        }
    }
    free(t->slots);
}

typedef struct {
    const char *king;
    Table people;
} Throne;

static void birth(Throne *t, const char *parent, const char *child) {
    Entry *e = find(&t->people, parent, 1);
    if (e->nkids == e->capkids) {
        e->capkids = e->capkids ? e->capkids * 2 : 4;
        e->kids = realloc(e->kids, sizeof(char *) * e->capkids);
    }
    e->kids[e->nkids++] = strdup(child);
}

static void death(Throne *t, const char *name) {
    find(&t->people, name, 1)->dead = 1;
}

// The order as malloc'd copies; *n is set to its length.
static char **order(Throne *t, int *n) {
    int cap = 64, len = 0, top = 0, scap = 64;
    char **out = malloc(sizeof(char *) * cap);
    const char **stack = malloc(sizeof(char *) * scap);
    stack[top++] = t->king;
    while (top > 0) {
        const char *name = stack[--top];
        Entry *e = find(&t->people, name, 0);
        if (!e || !e->dead) {
            if (len == cap) out = realloc(out, sizeof(char *) * (cap *= 2));
            out[len++] = strdup(name);
        }
        if (e) {
            for (int k = e->nkids - 1; k >= 0; k--) {
                if (top == scap) stack = realloc(stack, sizeof(char *) * (scap *= 2));
                stack[top++] = e->kids[k];
            }
        }
    }
    free(stack);
    *n = len;
    return out;
}

typedef struct {
    int kind;
    char *a, *b;
} Op;

static int64_t seed = 1600;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { R = 10, CALLS = 50000 };
    Op *reigns[R];
    int nops[R];
    for (int g = 0; g < R; g++) {
        char **alive = malloc(sizeof(char *) * (CALLS + 1));
        int nalive = 0, born = 0, n = 0;
        alive[nalive++] = strdup("king");
        Op *ops = malloc(sizeof(Op) * CALLS);
        for (int i = 0; i < CALLS; i++) {
            int64_t r = next_random() % 1000;
            if (r < 500 && nalive > 0) {
                char *parent = strdup(alive[next_random() % nalive]);
                char buf[24];
                snprintf(buf, sizeof buf, "p%d", ++born);
                ops[n++] = (Op){0, parent, strdup(buf)};
                alive[nalive++] = strdup(buf);
            } else if (r < 625 && nalive > 0) {
                int64_t at = next_random() % nalive;
                char *name = alive[at];
                alive[at] = alive[--nalive];
                ops[n++] = (Op){1, name, NULL};
            } else if (r < 626) {
                ops[n++] = (Op){2, NULL, NULL};
            }
        }
        for (int i = 0; i < nalive; i++) free(alive[i]);
        free(alive);
        reigns[g] = ops;
        nops[g] = n;
    }
    int64_t check = 0, names = 0;
    for (int g = 0; g < R; g++) {
        Throne t = {"king", {NULL, 0, 0}};
        for (int i = 0; i < nops[g]; i++) {
            Op *o = &reigns[g][i];
            if (o->kind == 0) {
                birth(&t, o->a, o->b);
            } else if (o->kind == 1) {
                death(&t, o->a);
            } else {
                int n;
                char **ord = order(&t, &n);
                names += n;
                for (int k = 0; k < n; k++) {
                    check = (check * 31 + (int64_t)strlen(ord[k]) + 1) % 1000000007;
                    free(ord[k]);
                }
                free(ord);
            }
        }
        table_free(&t.people);
    }
    printf("10 reigns of 50000 calls: %lld names in the orders, checksum %lld\n", (long long)names, (long long)check);
    for (int g = 0; g < R; g++) {
        for (int i = 0; i < nops[g]; i++) {
            free(reigns[g][i].a);
            free(reigns[g][i].b);
        }
        free(reigns[g]);
    }
    return 0;
}
