// LeetCode #1311 bench, C: the ★ arm (a breadth-first walk a level at a
// time, the videos of the people left counted in a hash table, then sorted
// as (count, title) pairs) on the same 50 groups and 200 passes. The table
// is its own: open addressing over FNV-1a hashes, sized to twice the videos
// counted; titles are shared pointers, and each answer a fresh malloc'd
// array of them.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100
#define VIDEOS 100

typedef struct {
    const char *title;
    int64_t count;
} Entry;

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) {
        h ^= (unsigned char)*s;
        h *= 1099511628211ULL;
    }
    return h;
}

static int by_count_then_title(const void *x, const void *y) {
    const Entry *a = x, *b = y;
    if (a->count != b->count) return a->count < b->count ? -1 : 1;
    return strcmp(a->title, b->title);
}

// answers into *out (malloc'd), returns its length
static int64_t watched_videos_by_friends(const char *watched[N][VIDEOS], int64_t *friends[N], const int64_t degree[N], int64_t id, int64_t level, const char ***out) {
    bool seen[N] = {false};
    int64_t people[N], next[N];
    int64_t count_people = 1, count_next;
    seen[id] = true;
    people[0] = id;
    for (int64_t l = 0; l < level; l++) {
        count_next = 0;
        for (int64_t k = 0; k < count_people; k++) {
            int64_t p = people[k];
            for (int64_t e = 0; e < degree[p]; e++) {
                int64_t f = friends[p][e];
                if (!seen[f]) {
                    seen[f] = true;
                    next[count_next++] = f;
                }
            }
        }
        memcpy(people, next, sizeof(int64_t) * (size_t)count_next);
        count_people = count_next;
    }
    size_t cap = 1;
    while (cap < 2 * (size_t)(count_people * VIDEOS) + 1) cap *= 2;
    Entry *table = calloc(cap, sizeof(Entry));
    int64_t distinct = 0;
    for (int64_t k = 0; k < count_people; k++) {
        for (int v = 0; v < VIDEOS; v++) {
            const char *title = watched[people[k]][v];
            size_t at = fnv(title) & (cap - 1);
            while (table[at].title && strcmp(table[at].title, title) != 0) at = (at + 1) & (cap - 1);
            if (!table[at].title) {
                table[at].title = title;
                distinct++;
            }
            table[at].count++;
        }
    }
    Entry *ranked = malloc(sizeof(Entry) * (size_t)(distinct + 1));
    int64_t r = 0;
    for (size_t at = 0; at < cap; at++) {
        if (table[at].title) ranked[r++] = table[at];
    }
    free(table);
    qsort(ranked, (size_t)r, sizeof(Entry), by_count_then_title);
    const char **titles = malloc(sizeof(char *) * (size_t)(r + 1));
    for (int64_t k = 0; k < r; k++) titles[k] = ranked[k].title;
    free(ranked);
    *out = titles;
    return r;
}

static int64_t seed = 1311;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t fold(int64_t check, const char *title) {
    for (; *title; title++) check = (check * 31 + (unsigned char)*title) % 1000000007;
    return check;
}

static const char *groups[50][N][VIDEOS];
static int64_t *links[50][N];
static int64_t degrees[50][N];

int main(void) {
    char titles[400][9];
    for (int t = 0; t < 400; t++) {
        int64_t len = 1 + next_random() % 8;
        for (int64_t k = 0; k < len; k++) titles[t][k] = (char)('a' + next_random() % 26);
        titles[t][len] = '\0';
    }
    for (int g = 0; g < 50; g++) {
        for (int p = 0; p < N; p++) links[g][p] = malloc(sizeof(int64_t) * N);
        for (int64_t a = 0; a < N; a++) {
            for (int64_t b = a + 1; b < N; b++) {
                if (next_random() % 25 == 0) {
                    links[g][a][degrees[g][a]++] = b;
                    links[g][b][degrees[g][b]++] = a;
                }
            }
        }
        for (int p = 0; p < N; p++) {
            for (int v = 0; v < VIDEOS; v++) groups[g][p][v] = titles[next_random() % 400];
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 200; pass++) {
        for (int g = 0; g < 50; g++) {
            groups[g][check % N][(check / 7) % VIDEOS] = titles[(check / 11) % 400];
            int64_t id = (check / 13) % N;
            int64_t level = 1 + (check / 17) % 3;
            const char **got;
            int64_t len = watched_videos_by_friends(groups[g], links[g], degrees[g], id, level, &got);
            check = (check * 31 + len) % 1000000007;
            if (len > 0) {
                check = fold(check, got[0]);
                check = fold(check, got[len - 1]);
            }
            check = (check + pass) % 1000000007;
            free(got);
        }
    }
    printf("200 passes over 50 groups of 100: checksum %lld\n", (long long)check);
    return 0;
}
