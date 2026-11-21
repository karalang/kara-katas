// LeetCode #2424: Longest Uploaded Prefix -- the bench, the ★ arm: a flag
// for each video and the prefix so far, moved on by `longest` past every
// flag set beyond it.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    bool *uploaded;
    int64_t prefix;
} LuPrefix;

static LuPrefix lu_new(int64_t n) {
    LuPrefix s = {calloc((size_t)(n + 2), sizeof(bool)), 0};
    return s;
}

static void lu_upload(LuPrefix *s, int64_t video) { s->uploaded[video] = true; }

static int64_t lu_longest(LuPrefix *s) {
    while (s->uploaded[s->prefix + 1]) s->prefix++;
    return s->prefix;
}

static int64_t seed = 2424;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int64_t *scripts[10];
    for (int s = 0; s < 10; s++) {
        int64_t width = (int64_t)1 << (s + 3);
        int64_t *order = malloc((size_t)n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) order[i] = i + 1;
        for (int64_t start = 0; start < n;) {
            int64_t end = start + width < n ? start + width : n;
            for (int64_t i = end - 1; i > start; i--) {
                int64_t a = next_random();
                int64_t r = a * 32768 + next_random();
                int64_t j = start + r % (i - start + 1);
                int64_t t = order[i]; order[i] = order[j]; order[j] = t;
            }
            start = end;
        }
        scripts[s] = order;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int s = 0; s < 10; s++) {
            LuPrefix server = lu_new(n);
            for (int64_t k = 0; k < n; k++) {
                lu_upload(&server, scripts[s][k]);
                check = (check * 31 + lu_longest(&server) + p) % 1000000007;
            }
            free(server.uploaded);
        }
    }
    printf("50 passes over 10 scripts of 10^5 uploads: checksum %lld\n", (long long)check);
    for (int s = 0; s < 10; s++) free(scripts[s]);
    return 0;
}
