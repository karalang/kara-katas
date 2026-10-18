// LeetCode #721: Accounts Merge -- union-find over the emails.
// Benchmark mirror of the Kara star arm: every email numbered the first
// time it is seen, each account's emails joined in a union-find, then the
// emails gathered by their root, each group sorted under its name. C has
// no map, so the email numbers live in an open-addressing table hashed
// by FNV-1a, and the groups in lists indexed by root, which plays the
// part of the Kara arm's map from root to group. Strings are copied
// where the Kara arm clones them.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

typedef struct {
    char **words;  // name, then emails
    int n;
} Account;

static uint64_t fnv1a(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static int64_t find(int64_t *parent, int64_t x) {
    int64_t root = x;
    while (parent[root] != root) root = parent[root];
    while (parent[x] != root) {
        int64_t up = parent[x];
        parent[x] = root;
        x = up;
    }
    return root;
}

static int cmp(const void *a, const void *b) {
    return strcmp(*(char *const *)a, *(char *const *)b);
}

// Merges the accounts and returns the bench's measure of the result: the
// number of people plus the length of each person's smallest email.
static int64_t accounts_merge(const Account *accounts, int count) {
    int64_t total = 0;
    for (int a = 0; a < count; a++) total += accounts[a].n - 1;
    int64_t cap = 16;
    while (cap < 2 * total) cap *= 2;
    char **keys = calloc(cap, sizeof(char *));
    int64_t *vals = malloc(cap * sizeof(int64_t));
    char **emails = malloc(total * sizeof(char *));
    char **owner = malloc(total * sizeof(char *));
    int64_t *parent = malloc(total * sizeof(int64_t));
    int64_t ne = 0;
    for (int a = 0; a < count; a++) {
        int64_t first = -1;
        for (int k = 1; k < accounts[a].n; k++) {
            const char *email = accounts[a].words[k];
            uint64_t h = fnv1a(email) & (cap - 1);
            while (keys[h] && strcmp(keys[h], email) != 0) h = (h + 1) & (cap - 1);
            if (!keys[h]) {
                keys[h] = strdup(email);
                vals[h] = ne;
                parent[ne] = ne;
                emails[ne] = strdup(email);
                owner[ne] = strdup(accounts[a].words[0]);
                ne++;
            }
            int64_t e = vals[h];
            if (first < 0) {
                first = e;
            } else {
                int64_t x = find(parent, first), y = find(parent, e);
                if (x != y) parent[y] = x;
            }
        }
    }
    // Gather by root: count each root's emails, then place them.
    int64_t *size = calloc(ne, sizeof(int64_t));
    int64_t *root_of = malloc(ne * sizeof(int64_t));
    for (int64_t e = 0; e < ne; e++) {
        root_of[e] = find(parent, e);
        size[root_of[e]]++;
    }
    int64_t *start = malloc((ne + 1) * sizeof(int64_t));
    start[0] = 0;
    for (int64_t r = 0; r < ne; r++) start[r + 1] = start[r] + size[r];
    char **grouped = malloc(ne * sizeof(char *));
    int64_t *fill = malloc(ne * sizeof(int64_t));
    memcpy(fill, start, ne * sizeof(int64_t));
    for (int64_t e = 0; e < ne; e++) grouped[fill[root_of[e]]++] = strdup(emails[e]);
    int64_t measure = 0;
    for (int64_t r = 0; r < ne; r++) {
        if (size[r] == 0) continue;
        char **person = malloc((size[r] + 1) * sizeof(char *));
        person[0] = strdup(owner[r]);
        qsort(grouped + start[r], size[r], sizeof(char *), cmp);
        for (int64_t k = 0; k < size[r]; k++) person[k + 1] = strdup(grouped[start[r] + k]);
        measure += 1 + (int64_t)strlen(person[1]);
        for (int64_t k = 0; k <= size[r]; k++) free(person[k]);
        free(person);
    }
    for (int64_t h = 0; h < cap; h++) free(keys[h]);
    for (int64_t e = 0; e < ne; e++) {
        free(emails[e]);
        free(owner[e]);
        free(grouped[e]);
    }
    free(keys); free(vals); free(emails); free(owner); free(parent);
    free(size); free(root_of); free(start); free(grouped); free(fill);
    return measure;
}

enum { LISTS = 20, ACCOUNTS = 1000 };

int main(void) {
    const char *names[] = {"Ada", "Bo", "Cy", "Di"};
    int64_t seed = 721;
    static Account lists[LISTS][ACCOUNTS];
    char buf[32];
    for (int l = 0; l < LISTS; l++) {
        for (int a = 0; a < ACCOUNTS; a++) {
            int64_t who = next_random(&seed) % 4;
            int64_t n = 1 + next_random(&seed) % 4;
            Account *acc = &lists[l][a];
            acc->n = (int)n + 1;
            acc->words = malloc((n + 1) * sizeof(char *));
            acc->words[0] = strdup(names[who]);
            for (int64_t k = 0; k < n; k++) {
                int64_t e = 4 * (next_random(&seed) % 2000) + who;
                snprintf(buf, sizeof buf, "u%lld@m.co", (long long)e);
                acc->words[k + 1] = strdup(buf);
            }
        }
    }
    int64_t sum = 0;
    for (int64_t round = 0; round < 50; round++) {
        for (int64_t d = 0; d < LISTS; d++) {
            int64_t i = (round * 7919 + d * 104729) % ACCOUNTS;
            int64_t j = (i + 1) % ACCOUNTS;
            while (strcmp(lists[d][j].words[0], lists[d][i].words[0]) != 0) j = (j + 1) % ACCOUNTS;
            Account *acc = &lists[d][i];
            free(acc->words[acc->n - 1]);
            acc->words[acc->n - 1] = strdup(lists[d][j].words[1]);
            sum += accounts_merge(lists[d], ACCOUNTS);
        }
    }
    printf("50 rounds of 20 lists of 1000 accounts: sum %lld\n", (long long)sum);
    return 0;
}
