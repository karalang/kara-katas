// LeetCode #2456: Most Popular Video Creator -- bench, C mirror of
// creator.kara: one pass keeps each creator's total and best video in an
// open-addressing hash table keyed by the creator's name, then every
// creator at the largest total, sorted.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000
#define CAP (1 << 15)

typedef struct {
    char name[8];
    int64_t total, top;
    const char *id;
    int used;
} Slot;

static Slot table[CAP];

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) {
        h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    }
    return h;
}

static Slot *find(const char *name) {
    size_t i = (size_t)(hash(name) & (CAP - 1));
    while (table[i].used && strcmp(table[i].name, name) != 0) {
        i = (i + 1) & (CAP - 1);
    }
    return &table[i];
}

typedef struct {
    const char *creator, *id;
} Pair;

static int by_pair(const void *a, const void *b) {
    const Pair *x = a, *y = b;
    int c = strcmp(x->creator, y->creator);
    return c != 0 ? c : strcmp(x->id, y->id);
}

static Pair answer[CAP];

static int64_t most_popular_creator(char (*creators)[4], char (*ids)[6], const int64_t *views, int64_t n) {
    memset(table, 0, sizeof table);
    for (int64_t i = 0; i < n; i++) {
        Slot *s = find(creators[i]);
        if (s->used) {
            int better = views[i] > s->top || (views[i] == s->top && strcmp(ids[i], s->id) < 0);
            s->total += views[i];
            if (better) {
                s->top = views[i];
                s->id = ids[i];
            }
        } else {
            s->used = 1;
            strcpy(s->name, creators[i]);
            s->total = views[i];
            s->top = views[i];
            s->id = ids[i];
        }
    }
    int64_t most = 0;
    for (int i = 0; i < CAP; i++) {
        if (table[i].used && table[i].total > most) most = table[i].total;
    }
    int64_t k = 0;
    for (int i = 0; i < CAP; i++) {
        if (table[i].used && table[i].total == most) {
            answer[k].creator = table[i].name;
            answer[k].id = table[i].id;
            k++;
        }
    }
    qsort(answer, (size_t)k, sizeof(Pair), by_pair);
    return k;
}

static int64_t seed = 2456;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_name(char *out, int len, int64_t letters) {
    for (int i = 0; i < len; i++) out[i] = (char)(97 + next_random() % letters);
    out[len] = 0;
}

int main(void) {
    char (*creators[10])[4];
    char (*ids[10])[6];
    int64_t *views[10];
    for (int a = 0; a < 10; a++) {
        creators[a] = malloc(sizeof(char[4]) * N);
        ids[a] = malloc(sizeof(char[6]) * N);
        views[a] = malloc(sizeof(int64_t) * N);
        for (int i = 0; i < N; i++) random_name(creators[a][i], 3, 26);
        for (int i = 0; i < N; i++) random_name(ids[a][i], 5, 26);
        for (int i = 0; i < N; i++) views[a][i] = next_random() % 100001;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 16; p++) {
        for (int64_t a = 0; a < 10; a++) {
            views[a][(p * 7919 + a) % N] = check % 100001;
            int64_t k = most_popular_creator(creators[a], ids[a], views[a], N);
            for (int64_t j = 0; j < k; j++) {
                const char *w[2] = {answer[j].creator, answer[j].id};
                for (int t = 0; t < 2; t++) {
                    for (const char *c = w[t]; *c; c++) {
                        check = (check * 31 + (unsigned char)*c) % 1000000007;
                    }
                }
            }
            check = (check + p) % 1000000007;
        }
    }
    printf("16 passes over 10 lists of 10^5 videos: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(creators[a]);
        free(ids[a]);
        free(views[a]);
    }
    return 0;
}
