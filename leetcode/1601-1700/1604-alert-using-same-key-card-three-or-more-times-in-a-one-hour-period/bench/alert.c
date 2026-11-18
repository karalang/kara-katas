// LeetCode #1604: Alert Using Same Key-Card Three or More Times in a One
// Hour Period -- the bench in C, mirroring alert.kara: each name's minutes
// in an open-addressing hash table (C has no ordered map), the names then
// sorted, each list sorted.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *NAMES[8] = {"daniel", "luis", "alice", "bob", "john", "leslie", "clare", "anna"};

typedef struct {
    char *name;
    int32_t *times;
    int64_t len, cap;
} Entry;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static int cmp_entry(const void *a, const void *b) {
    return strcmp((*(Entry *const *)a)->name, (*(Entry *const *)b)->name);
}

static int cmp_i32(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

// the names alerted, in order, written to `out`; returns how many
static int64_t alert_names(char **key_name, char **key_time, int64_t n, char **out) {
    int64_t cap = 16;
    while (cap < 2 * n) cap *= 2;
    Entry *table = calloc(cap, sizeof(Entry));
    Entry **used = malloc(n * sizeof(Entry *));
    int64_t nused = 0;
    for (int64_t i = 0; i < n; i++) {
        uint64_t k = hash(key_name[i]) & (cap - 1);
        while (table[k].name && strcmp(table[k].name, key_name[i]) != 0) k = (k + 1) & (cap - 1);
        Entry *e = &table[k];
        if (!e->name) {
            e->name = key_name[i];
            used[nused++] = e;
        }
        const char *t = key_time[i];
        int32_t m = (int32_t)(atoi(t) * 60 + atoi(t + 3));
        if (e->len == e->cap) {
            e->cap = e->cap ? e->cap * 2 : 4;
            e->times = realloc(e->times, e->cap * sizeof(int32_t));
        }
        e->times[e->len++] = m;
    }
    qsort(used, nused, sizeof(Entry *), cmp_entry);
    int64_t count = 0;
    for (int64_t u = 0; u < nused; u++) {
        Entry *e = used[u];
        qsort(e->times, e->len, sizeof(int32_t), cmp_i32);
        for (int64_t i = 2; i < e->len; i++) {
            if (e->times[i] - e->times[i - 2] <= 60) {
                out[count++] = e->name;
                break;
            }
        }
        free(e->times);
    }
    free(used);
    free(table);
    return count;
}

static int64_t seed = 1604;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t big(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    enum { DAYS = 30, SWIPES = 100000 };
    char **names = malloc((size_t)DAYS * SWIPES * sizeof(char *));
    char **times = malloc((size_t)DAYS * SWIPES * sizeof(char *));
    for (int64_t i = 0; i < (int64_t)DAYS * SWIPES; i++) {
        int64_t who = big() % 20000;
        char buf[32];
        if (who < 8) snprintf(buf, sizeof buf, "%s", NAMES[who]);
        else snprintf(buf, sizeof buf, "%s%lld", NAMES[who % 8], (long long)(who / 8));
        names[i] = strdup(buf);
        int64_t t = big() % 1440;
        snprintf(buf, sizeof buf, "%02lld:%02lld", (long long)(t / 60), (long long)(t % 60));
        times[i] = strdup(buf);
    }
    char **out = malloc(SWIPES * sizeof(char *));
    int64_t check = 0, alerts = 0;
    for (int d = 0; d < DAYS; d++) {
        int64_t k = alert_names(names + (int64_t)d * SWIPES, times + (int64_t)d * SWIPES, SWIPES, out);
        for (int64_t i = 0; i < k; i++) {
            alerts++;
            for (const unsigned char *b = (const unsigned char *)out[i]; *b; b++) check = mix(check, *b);
            check = mix(check, 0);
        }
    }
    printf("30 days of 100000 swipes by 20000 names: %lld alerts, checksum %lld\n", (long long)alerts, (long long)check);
    for (int64_t i = 0; i < (int64_t)DAYS * SWIPES; i++) {
        free(names[i]);
        free(times[i]);
    }
    free(names);
    free(times);
    free(out);
    return 0;
}
