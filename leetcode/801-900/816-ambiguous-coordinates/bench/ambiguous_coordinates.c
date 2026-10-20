// Benchmark for #816: Ambiguous Coordinates -- mirror of the ★ arm (every
// split and every point), with the same workload as
// ambiguous_coordinates.kara. Every number and coordinate is its own
// malloc'd string, freed once the round has folded it in.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **items;
    int64_t len, cap;
} Strings;

static void push(Strings *v, char *s) {
    if (v->len == v->cap) {
        v->cap = v->cap ? 2 * v->cap : 8;
        v->items = realloc(v->items, v->cap * sizeof(char *));
    }
    v->items[v->len++] = s;
}

static void free_all(Strings *v) {
    for (int64_t i = 0; i < v->len; i++) {
        free(v->items[i]);
    }
    free(v->items);
}

// Every number the n digits at part can spell with at most one point.
static Strings numbers(const char *part, int64_t n) {
    Strings found = {0};
    for (int64_t point = 1; point <= n; point++) {
        int whole_ok = point == 1 || part[0] != '0';
        int fraction_ok = point == n || part[n - 1] != '0';
        if (whole_ok && fraction_ok) {
            char *s = malloc(n + 2);
            memcpy(s, part, point);
            if (point == n) {
                s[point] = '\0';
            } else {
                s[point] = '.';
                memcpy(s + point + 1, part + point, n - point);
                s[n + 1] = '\0';
            }
            push(&found, s);
        }
    }
    return found;
}

static Strings ambiguous_coordinates(const char *s) {
    const char *digits = s + 1;
    int64_t n = (int64_t)strlen(s) - 2;
    Strings out = {0};
    for (int64_t cut = 1; cut < n; cut++) {
        Strings lefts = numbers(digits, cut);
        Strings rights = numbers(digits + cut, n - cut);
        for (int64_t i = 0; i < lefts.len; i++) {
            for (int64_t j = 0; j < rights.len; j++) {
                size_t size = strlen(lefts.items[i]) + strlen(rights.items[j]) + 5;
                char *c = malloc(size);
                snprintf(c, size, "(%s, %s)", lefts.items[i], rights.items[j]);
                push(&out, c);
            }
        }
        free_all(&lefts);
        free_all(&rights);
    }
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 64 };
    const int64_t rounds = 400000;
    int64_t seed = 816;
    int64_t strings[COUNT][10];
    for (int g = 0; g < COUNT; g++) {
        for (int k = 0; k < 10; k++) {
            strings[g][k] = next_random(&seed) % 4 == 0 ? 0 : next_random(&seed) % 10;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int g = (int)(round % COUNT);
        int64_t at = next_random(&seed) % 10;
        strings[g][at] = next_random(&seed) % 4 == 0 ? 0 : next_random(&seed) % 10;
        char s[13];
        s[0] = '(';
        for (int k = 0; k < 10; k++) {
            s[k + 1] = (char)('0' + strings[g][k]);
        }
        s[11] = ')';
        s[12] = '\0';
        Strings answer = ambiguous_coordinates(s);
        total += answer.len;
        for (int64_t i = 0; i < answer.len; i++) {
            checksum = (checksum * 131 + (int64_t)strlen(answer.items[i])) % 1000000007;
        }
        free_all(&answer);
    }
    printf("%lld rounds of 10 digits: %lld coordinates, checksum %lld\n", (long long)rounds,
           (long long)total, (long long)checksum);
    return 0;
}
