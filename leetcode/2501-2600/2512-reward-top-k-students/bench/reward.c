// LeetCode #2512: Reward Top K Students -- C mirror of the benchmark
// (reward.kara): the same cases, passes and checksum, the words in two
// open-addressed tables of 1024 slots probed linearly, built afresh on
// every ask, and each report's words looked up as they are split.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 1024
#define WORD 8

typedef struct { char text[WORD]; int len; } Slot;

static uint64_t hash_of(const char *s, int len) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < len; i++) h = (h ^ (unsigned char)s[i]) * 1099511628211ULL;
    return h;
}

static void insert(Slot *t, const char *s, int len) {
    uint64_t at = hash_of(s, len) & (SLOTS - 1);
    while (t[at].len != 0) {
        if (t[at].len == len && memcmp(t[at].text, s, len) == 0) return;
        at = (at + 1) & (SLOTS - 1);
    }
    memcpy(t[at].text, s, len);
    t[at].len = len;
}

static int contains(const Slot *t, const char *s, int len) {
    uint64_t at = hash_of(s, len) & (SLOTS - 1);
    while (t[at].len != 0) {
        if (t[at].len == len && memcmp(t[at].text, s, len) == 0) return 1;
        at = (at + 1) & (SLOTS - 1);
    }
    return 0;
}

typedef struct { int64_t score, id; } Ranked;

static int by_rank(const void *x, const void *y) {
    const Ranked *a = x, *b = y;
    if (a->score != b->score) return a->score < b->score ? -1 : 1;
    return a->id < b->id ? -1 : (a->id > b->id);
}

typedef struct {
    char **positive, **negative, **report;
    int64_t p, q, *ids, k;
} Case;

static Slot good[SLOTS], bad[SLOTS];
static Ranked ranked[1000];

static int64_t top_students(const Case *c, int64_t *out) {
    memset(good, 0, sizeof good);
    memset(bad, 0, sizeof bad);
    for (int64_t i = 0; i < c->p; i++) insert(good, c->positive[i], (int)strlen(c->positive[i]));
    for (int64_t i = 0; i < c->q; i++) insert(bad, c->negative[i], (int)strlen(c->negative[i]));
    for (int64_t i = 0; i < 1000; i++) {
        int64_t score = 0;
        const char *s = c->report[i];
        while (*s) {
            const char *e = s;
            while (*e && *e != ' ') e++;
            int len = (int)(e - s);
            if (contains(good, s, len)) score += 3;
            else if (contains(bad, s, len)) score -= 1;
            s = *e ? e + 1 : e;
        }
        ranked[i] = (Ranked){-score, c->ids[i]};
    }
    qsort(ranked, 1000, sizeof ranked[0], by_rank);
    for (int64_t i = 0; i < c->k; i++) out[i] = ranked[i].id;
    return c->k;
}

static int64_t seed = 2512;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *word(int64_t w) {
    char digits[WORD];
    int n = 0;
    for (int64_t v = w + 5; v > 0; v /= 5) digits[n++] = (char)('a' + v % 5);
    char *text = malloc(n + 1);
    for (int i = 0; i < n; i++) text[i] = digits[n - 1 - i];
    text[n] = 0;
    return text;
}

int main(void) {
    Case cases[100];
    for (int64_t c = 0; c < 100; c++) {
        Case *x = &cases[c];
        x->p = next_random() % 200 + 1;
        x->q = next_random() % 200 + 1;
        x->positive = malloc(x->p * sizeof(char *));
        x->negative = malloc(x->q * sizeof(char *));
        for (int64_t w = 0; w < x->p; w++) x->positive[w] = word(w);
        for (int64_t w = 0; w < x->q; w++) x->negative[w] = word(x->p + w);
        x->report = malloc(1000 * sizeof(char *));
        for (int64_t r = 0; r < 1000; r++) {
            int64_t length = next_random() % 20 + 1;
            char *line = malloc(length * 5 + 1);
            line[0] = 0;
            for (int64_t i = 0; i < length; i++) {
                char *w = word(next_random() % 600);
                if (i > 0) strcat(line, " ");
                strcat(line, w);
                free(w);
            }
            x->report[r] = line;
        }
        x->ids = malloc(1000 * sizeof(int64_t));
        for (int64_t r = 0; r < 1000; r++) x->ids[r] = (r * 7919 + c) % 1000003 + 1;
        x->k = c * 10 + 1;
    }
    const int64_t passes = 50;
    int64_t check = 0, out[1000];
    for (int64_t p = 0; p < passes; p++) {
        for (int64_t c = 0; c < 100; c++) {
            Case *x = &cases[c];
            int64_t at = check % 1000;
            char *kept = x->report[at];
            x->report[at] = x->report[(check / 1000 + p) % 1000];
            int64_t n = top_students(x, out);
            for (int64_t i = 0; i < n; i++) check = (check * 31 + out[i] + p) % 1000000007;
            x->report[at] = kept;
        }
    }
    printf("%lld passes over 100 cases of 1000 reports: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
