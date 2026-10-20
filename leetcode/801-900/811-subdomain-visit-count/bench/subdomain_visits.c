// LeetCode 811 -- Subdomain Visit Count: the bench, with the ★ arm's map
// from domain to visits, an open-addressing hash table of the domains.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 811;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

typedef struct {
    char *key;
    size_t len;
    int64_t total;
} Slot;

static uint64_t hash(const char *s, size_t n) {
    uint64_t h = 14695981039346656037ULL;
    for (size_t i = 0; i < n; i++) {
        h = (h ^ (unsigned char)s[i]) * 1099511628211ULL;
    }
    return h;
}

// The answer's lines, malloc'd, into `out`; returns how many.
static int64_t subdomain_visits(char **cpdomains, int64_t n, char **out) {
    size_t cap = 1024;
    Slot *table = calloc(cap, sizeof(Slot));
    int64_t used = 0;
    for (int64_t k = 0; k < n; k++) {
        const char *entry = cpdomains[k];
        const char *space = strchr(entry, ' ');
        int64_t count = strtoll(entry, NULL, 10);
        const char *domain = space + 1;
        for (;;) {
            size_t len = strlen(domain);
            size_t at = hash(domain, len) & (cap - 1);
            while (table[at].key &&
                   !(table[at].len == len && memcmp(table[at].key, domain, len) == 0)) {
                at = (at + 1) & (cap - 1);
            }
            if (!table[at].key) {
                table[at].key = malloc(len + 1);
                memcpy(table[at].key, domain, len + 1);
                table[at].len = len;
                used++;
            }
            table[at].total += count;
            const char *dot = strchr(domain, '.');
            if (!dot) {
                break;
            }
            domain = dot + 1;
        }
    }
    int64_t lines = 0;
    for (size_t at = 0; at < cap; at++) {
        if (table[at].key) {
            char buf[64];
            int w = snprintf(buf, sizeof buf, "%lld %s", (long long)table[at].total, table[at].key);
            out[lines] = malloc(w + 1);
            memcpy(out[lines], buf, w + 1);
            lines++;
            free(table[at].key);
        }
    }
    free(table);
    (void)used;
    return lines;
}

static const char *tops[] = {"com", "org", "net", "io"};
static const char *middles[] = {"leetcode", "google", "yahoo", "wiki", "kara"};
static const char *lefts[] = {"mail", "discuss", "www", "api", "m", "docs"};

// A domain of 2 or 3 parts: a left part one time in three, then a middle
// part and a top part.
static char *random_domain(void) {
    char buf[64];
    const char *top = tops[next_random() % 4];
    const char *middle = middles[next_random() % 5];
    if (next_random() % 3 == 0) {
        snprintf(buf, sizeof buf, "%s.%s", middle, top);
    } else {
        const char *left = lefts[next_random() % 6];
        snprintf(buf, sizeof buf, "%s.%s.%s", left, middle, top);
    }
    return strdup(buf);
}

static char *entry_of(int64_t count, const char *domain) {
    char buf[64];
    snprintf(buf, sizeof buf, "%lld %s", (long long)count, domain);
    return strdup(buf);
}

// 64 lists of 100 entries are made once. Each round writes a new count
// into one entry of the next list and counts that list's visits; the
// answer's lines, in whatever order they come, are folded into a sum.
int main(void) {
    static char *lists[64][100];
    static char *domains[64][100];
    for (int k = 0; k < 64; k++) {
        for (int j = 0; j < 100; j++) {
            domains[k][j] = random_domain();
            lists[k][j] = entry_of(1 + next_random() % 10000, domains[k][j]);
        }
    }
    int64_t rounds = 100000;
    int64_t lines = 0;
    int64_t check = 0;
    char *out[300];
    for (int64_t r = 0; r < rounds; r++) {
        int64_t k = r % 64;
        int64_t i = r / 64 % 100;
        free(lists[k][i]);
        lists[k][i] = entry_of(1 + next_random() % 10000, domains[k][i]);
        int64_t m = subdomain_visits(lists[k], 100, out);
        int64_t sum = 0;
        for (int64_t j = 0; j < m; j++) {
            sum += strtoll(out[j], NULL, 10) * 7 + (int64_t)strlen(out[j]);
            free(out[j]);
        }
        lines += m;
        check = (check * 131 + sum) % 1000000007;
    }
    printf("%lld rounds of 100 entries: %lld lines, checksum %lld\n",
           (long long)rounds, (long long)lines, (long long)check);
    return 0;
}
