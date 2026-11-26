#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* The C mirror of build_array.kara: a fresh string for every operation,
   strdup'd as the Kara arm's to_string makes one, in a growing array. */
typedef struct {
    char **ops;
    int len, cap;
} Ops;

static void push(Ops *o, const char *s) {
    if (o->len == o->cap) {
        o->cap = o->cap ? o->cap * 2 : 4;
        o->ops = realloc(o->ops, sizeof(char *) * (size_t)o->cap);
    }
    o->ops[o->len++] = strdup(s);
}

static Ops build_array(const int32_t *target, int m, int32_t n) {
    Ops o = {0};
    int next = 0;
    for (int32_t x = 1; x <= n; x++) {
        if (next == m) break;
        push(&o, "Push");
        if (target[next] == x) next++;
        else push(&o, "Pop");
    }
    return o;
}

int main(void) {
    int64_t seed = 1441;
    static int32_t targets[1000][100];
    static int lens[1000];
    for (int t = 0; t < 1000; t++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t keep = 1 + seed / 65536 % 100;
        int m = 0;
        for (int32_t x = 1; x <= 100; x++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            if (seed / 65536 % 100 < keep) targets[t][m++] = x;
        }
        if (m == 0) targets[t][m++] = 100;
        lens[t] = m;
    }
    int64_t check = 0;
    for (int r = 0; r < 200; r++)
        for (int t = 0; t < 1000; t++) {
            Ops o = build_array(targets[t], lens[t], 100);
            int64_t h = 0;
            for (int i = 0; i < o.len; i++) {
                h = (h * 3 + (strcmp(o.ops[i], "Push") == 0 ? 1 : 2)) % 1000000007;
                free(o.ops[i]);
            }
            free(o.ops);
            check = (check * 131 + h) % 1000000007;
        }
    printf("2 * 10^5 targets: checksum %lld\n", (long long)check);
    return 0;
}
