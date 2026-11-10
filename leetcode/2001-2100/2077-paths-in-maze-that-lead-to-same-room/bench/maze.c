// LeetCode #2077: Paths in Maze That Lead to Same Room -- C mirror of the
// ★ arm's benchmark (maze.kara): 30 mazes of 1000 rooms and about 38000
// corridors; each room's rooms above it an open-addressing hash set,
// grown when half full, and every corridor's triangles the rooms of one
// set found in the other. The generator's corridors seen are a byte
// matrix.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long seed = 2077;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long min(long long a, long long b) { return a < b ? a : b; }
static long long max(long long a, long long b) { return a > b ? a : b; }

typedef struct {
    long long *slots;  // -1 empty
    long long cap, len;
} Set;

static unsigned long long mix(long long x) {
    unsigned long long h = (unsigned long long)x * 0x9E3779B97F4A7C15ULL;
    return h ^ (h >> 29);
}

static void set_init(Set *s) {
    s->cap = 8;
    s->len = 0;
    s->slots = malloc(sizeof(long long) * s->cap);
    memset(s->slots, 0xff, sizeof(long long) * s->cap);
}

static int set_has(const Set *s, long long x) {
    unsigned long long i = mix(x) & (s->cap - 1);
    while (s->slots[i] != -1) {
        if (s->slots[i] == x) return 1;
        i = (i + 1) & (s->cap - 1);
    }
    return 0;
}

static void set_put(Set *s, long long x);

static void set_grow(Set *s) {
    long long *old = s->slots;
    long long cap = s->cap;
    s->cap *= 2;
    s->len = 0;
    s->slots = malloc(sizeof(long long) * s->cap);
    memset(s->slots, 0xff, sizeof(long long) * s->cap);
    for (long long i = 0; i < cap; i++)
        if (old[i] != -1) set_put(s, old[i]);
    free(old);
}

static void set_put(Set *s, long long x) {
    if (2 * (s->len + 1) > s->cap) set_grow(s);
    unsigned long long i = mix(x) & (s->cap - 1);
    while (s->slots[i] != -1) {
        if (s->slots[i] == x) return;
        i = (i + 1) & (s->cap - 1);
    }
    s->slots[i] = x;
    s->len++;
}

static long long random_maze(long long n, long long count, long long near, long long *corridors,
                             unsigned char *seen) {
    memset(seen, 0, (size_t)((n + 1) * (n + 1)));
    long long m = 0;
    for (long long k = 0; k < count; k++) {
        long long a = next_random() % n + 1;
        long long step = next_random() % min(near, n - 1) + 1;
        long long b = (a - 1 + step) % n + 1;
        long long key = min(a, b) * (n + 1) + max(a, b);
        if (!seen[key]) {
            seen[key] = 1;
            if (next_random() % 2 == 0) {
                corridors[2 * m] = a;
                corridors[2 * m + 1] = b;
            } else {
                corridors[2 * m] = b;
                corridors[2 * m + 1] = a;
            }
            m++;
        }
    }
    return m;
}

static long long number_of_paths(long long n, const long long *corridors, long long m) {
    Set *up = malloc(sizeof(Set) * (n + 1));
    for (long long i = 0; i <= n; i++) set_init(&up[i]);
    for (long long k = 0; k < m; k++)
        set_put(&up[min(corridors[2 * k], corridors[2 * k + 1])],
                max(corridors[2 * k], corridors[2 * k + 1]));
    long long count = 0;
    for (long long a = 1; a <= n; a++) {
        Set *sa = &up[a];
        for (long long i = 0; i < sa->cap; i++) {
            long long b = sa->slots[i];
            if (b == -1) continue;
            for (long long j = 0; j < sa->cap; j++) {
                long long x = sa->slots[j];
                if (x != -1 && set_has(&up[b], x)) count++;
            }
        }
    }
    for (long long i = 0; i <= n; i++) free(up[i].slots);
    free(up);
    return count;
}

int main(void) {
    long long *corridors = malloc(sizeof(long long) * 120000);
    unsigned char *seen = malloc(1001 * 1001);
    long long total = 0, check = 0;
    for (int t = 0; t < 30; t++) {
        long long m = random_maze(1000, 60000, 60, corridors, seen);
        long long a = number_of_paths(1000, corridors, m);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    printf("30 mazes: sum %lld, checksum %lld\n", total, check);
    free(corridors);
    free(seen);
    return 0;
}
