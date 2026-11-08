// LeetCode #2019: The Score of Students Solving Math Expression -- the ★ arm's
// benchmark, a mirror of score.kara: each run's values in a hash set of its
// own (open addressing, linear probing, grown at half full).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *slots; // -1 marks an empty slot
    size_t cap, len;
} Set;

static void set_init(Set *s) {
    s->cap = 8;
    s->len = 0;
    s->slots = malloc(s->cap * sizeof(int64_t));
    memset(s->slots, 0xff, s->cap * sizeof(int64_t));
}

static size_t hash(int64_t v, size_t cap) { return (size_t)((uint64_t)v * 0x9E3779B97F4A7C15ull >> 20) & (cap - 1); }

static void set_insert(Set *s, int64_t v);

static void set_grow(Set *s) {
    int64_t *old = s->slots;
    size_t old_cap = s->cap;
    s->cap *= 2;
    s->len = 0;
    s->slots = malloc(s->cap * sizeof(int64_t));
    memset(s->slots, 0xff, s->cap * sizeof(int64_t));
    for (size_t i = 0; i < old_cap; i++)
        if (old[i] >= 0) set_insert(s, old[i]);
    free(old);
}

static void set_insert(Set *s, int64_t v) {
    if (2 * (s->len + 1) > s->cap) set_grow(s);
    size_t i = hash(v, s->cap);
    while (s->slots[i] >= 0) {
        if (s->slots[i] == v) return;
        i = (i + 1) & (s->cap - 1);
    }
    s->slots[i] = v;
    s->len++;
}

static int set_contains(const Set *s, int64_t v) {
    size_t i = hash(v, s->cap);
    while (s->slots[i] >= 0) {
        if (s->slots[i] == v) return 1;
        i = (i + 1) & (s->cap - 1);
    }
    return 0;
}

static int64_t score_of_students(const char *s, const int64_t *answers, size_t count) {
    size_t n = (strlen(s) + 1) / 2;
    int64_t digits[16];
    for (size_t i = 0; i < n; i++) digits[i] = s[2 * i] - '0';
    int64_t sum = 0, product = digits[0];
    for (size_t i = 0; i + 1 < n; i++) {
        if (s[2 * i + 1] == '+') {
            sum += product;
            product = digits[i + 1];
        } else {
            product *= digits[i + 1];
        }
    }
    int64_t correct = sum + product;
    Set values[16][16];
    for (size_t i = 0; i < n; i++)
        for (size_t j = 0; j < n; j++) {
            set_init(&values[i][j]);
            if (i == j) set_insert(&values[i][j], digits[i]);
        }
    for (size_t length = 2; length <= n; length++) {
        for (size_t i = 0; i + length - 1 < n; i++) {
            size_t j = i + length - 1;
            Set cell;
            set_init(&cell);
            for (size_t k = i; k < j; k++) {
                int plus = s[2 * k + 1] == '+';
                Set *left = &values[i][k], *right = &values[k + 1][j];
                for (size_t x = 0; x < left->cap; x++) {
                    int64_t a = left->slots[x];
                    if (a < 0) continue;
                    for (size_t y = 0; y < right->cap; y++) {
                        int64_t b = right->slots[y];
                        if (b < 0) continue;
                        int64_t v = plus ? a + b : a * b;
                        if (v <= 1000) set_insert(&cell, v);
                    }
                }
            }
            free(values[i][j].slots);
            values[i][j] = cell;
        }
    }
    int64_t points = 0;
    for (size_t a = 0; a < count; a++) {
        if (answers[a] == correct)
            points += 5;
        else if (set_contains(&values[0][n - 1], answers[a]))
            points += 2;
    }
    for (size_t i = 0; i < n; i++)
        for (size_t j = 0; j < n; j++) free(values[i][j].slots);
    return points;
}

static int64_t seed = 2019;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char expressions[200][32];
    static int64_t answer_lists[200][2000];
    for (int e = 0; e < 200; e++) {
        int64_t top = e % 9 + 1, times = e % 7 + 2;
        int at = 0;
        for (int i = 0; i < 16; i++) {
            if (i > 0) expressions[e][at++] = next_random() % 10 < times ? '*' : '+';
            expressions[e][at++] = (char)('0' + next_random() % (top + 1));
        }
        expressions[e][at] = '\0';
        for (int i = 0; i < 2000; i++) answer_lists[e][i] = next_random() % 1001;
    }
    int64_t calls = 0, total = 0, check = 0;
    for (int r = 0; r < 10; r++) {
        for (int e = 0; e < 200; e++) {
            int64_t points = score_of_students(expressions[e], answer_lists[e], 2000);
            calls++;
            total += points;
            check = (check * 31 + points) % 1000000007;
        }
    }
    printf("%lld calls: %lld points, checksum %lld\n", (long long)calls, (long long)total, (long long)check);
    return 0;
}
