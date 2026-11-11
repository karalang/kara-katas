// LeetCode #2115: Find All Possible Recipes from Given Supplies -- the
// benchmark, the same algorithm as recipes.kara: Kahn's order over names,
// a hash table (FNV-1a, open addressing) from each ingredient to the
// recipes needing it and a queue starting with the supplies.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 1024
#define NAME 8

typedef struct {
    char key[NAME];
    int used;
    int *users;
    int count, cap;
} slot;

static uint64_t fnv(const char *s) {
    uint64_t h = 14695981039346656037ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static slot *find(slot *table, const char *key, int insert) {
    uint64_t at = fnv(key) & (SLOTS - 1);
    while (table[at].used) {
        if (strcmp(table[at].key, key) == 0) return &table[at];
        at = (at + 1) & (SLOTS - 1);
    }
    if (!insert) return NULL;
    table[at].used = 1;
    strcpy(table[at].key, key);
    return &table[at];
}

typedef struct {
    char items[8][NAME];
    int count;
} need;

static int find_all_recipes(char recipes[][NAME], int n, need *ingredients, char supplies[][NAME], int s) {
    static slot table[SLOTS];
    for (int k = 0; k < SLOTS; k++) {
        free(table[k].users);
        memset(&table[k], 0, sizeof(slot));
    }
    int lacking[100];
    for (int i = 0; i < n; i++) {
        lacking[i] = ingredients[i].count;
        for (int j = 0; j < ingredients[i].count; j++) {
            slot *e = find(table, ingredients[i].items[j], 1);
            if (e->count == e->cap) {
                e->cap = e->cap ? e->cap * 2 : 4;
                e->users = realloc(e->users, sizeof(int) * e->cap);
            }
            e->users[e->count++] = i;
        }
    }
    char queue[256][NAME];
    int head = 0, tail = 0, made = 0;
    for (int k = 0; k < s; k++) strcpy(queue[tail++], supplies[k]);
    while (head < tail) {
        slot *e = find(table, queue[head++], 0);
        if (!e) continue;
        for (int u = 0; u < e->count; u++) {
            int i = e->users[u];
            if (--lacking[i] == 0) {
                made++;
                strcpy(queue[tail++], recipes[i]);
            }
        }
    }
    return made;
}

static int64_t seed = 2115;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char recipes[100][NAME], supplies[56][NAME];
    for (int i = 0; i < 100; i++) snprintf(recipes[i], NAME, "r%d", i);
    for (int i = 0; i < 56; i++) snprintf(supplies[i], NAME, "s%d", i);
    static need kitchens[40][100];
    for (int k = 0; k < 40; k++) {
        for (int64_t i = 0; i < 100; i++) {
            need *nd = &kitchens[k][i];
            nd->count = 0;
            int64_t count = next_random() % 8 + 1;
            for (int64_t c = 0; c < count; c++) {
                int64_t pick = next_random() % (60 + i);
                char item[NAME];
                if (pick < 60) snprintf(item, NAME, "s%lld", (long long)pick);
                else snprintf(item, NAME, "r%lld", (long long)(pick - 60));
                int seen = 0;
                for (int j = 0; j < nd->count; j++)
                    if (strcmp(nd->items[j], item) == 0) seen = 1;
                if (!seen) strcpy(nd->items[nd->count++], item);
            }
            if (nd->count == 0) strcpy(nd->items[nd->count++], "s0");
        }
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 10; round++) {
        for (int k = 0; k < 40; k++) {
            int i = (round * 37 + k) % 100;
            snprintf(kitchens[k][i].items[0], NAME, "s%d", (round + k) % 50);
            int64_t got = find_all_recipes(recipes, 100, kitchens[k], supplies, 56);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("400 solves: %lld recipes made, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
