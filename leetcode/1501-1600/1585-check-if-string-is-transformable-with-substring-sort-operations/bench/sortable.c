// LeetCode #1585 bench: the same first-unused-copy match, in C. Each digit's
// queue is a growable array with a head index, allocated per call as the
// Kara VecDeques are; the substring sorts are insertion sorts, which for
// runs of at most 50 bytes is what every library sort falls back to.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *v;
    int64_t head, len, cap;
} Queue;

static void push(Queue *q, int64_t x) {
    if (q->len == q->cap) {
        q->cap = q->cap ? q->cap * 2 : 4;
        q->v = realloc(q->v, q->cap * sizeof(int64_t));
    }
    q->v[q->len++] = x;
}

static int is_transformable(const unsigned char *s, const unsigned char *t, int64_t n) {
    Queue at[10];
    memset(at, 0, sizeof at);
    for (int64_t i = 0; i < n; i++) push(&at[s[i] - '0'], i);
    int ok = 1;
    for (int64_t i = 0; i < n && ok; i++) {
        int d = t[i] - '0';
        if (at[d].head == at[d].len) {
            ok = 0;
            break;
        }
        int64_t p = at[d].v[at[d].head++];
        for (int e = 0; e < d; e++) {
            if (at[e].head < at[e].len && at[e].v[at[e].head] < p) {
                ok = 0;
                break;
            }
        }
    }
    for (int d = 0; d < 10; d++) free(at[d].v);
    return ok;
}

static int64_t seed = 1585;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static void sort_run(unsigned char *a, int64_t len) {
    for (int64_t i = 1; i < len; i++) {
        unsigned char x = a[i];
        int64_t j = i;
        while (j > 0 && a[j - 1] > x) {
            a[j] = a[j - 1];
            j--;
        }
        a[j] = x;
    }
}

int main(void) {
    enum { P = 40, N = 100000 };
    unsigned char *ss[P], *ts[P];
    for (int k = 0; k < P; k++) {
        ss[k] = malloc(N);
        for (int64_t i = 0; i < N; i++) ss[k][i] = '0' + next_random() % 10;
        ts[k] = malloc(N);
        memcpy(ts[k], ss[k], N);
        for (int r = 0; r < 2000; r++) {
            int64_t a = (next_random() * 32768 + next_random()) % (N - 50);
            int64_t b = a + next_random() % 50 + 1;
            sort_run(ts[k] + a, b - a);
        }
        if (k % 2 == 1) {
            int64_t a = (next_random() * 32768 + next_random()) % N;
            int64_t b = (next_random() * 32768 + next_random()) % N;
            unsigned char x = ts[k][a];
            ts[k][a] = ts[k][b];
            ts[k][b] = x;
        }
    }
    int64_t check = 0, yes = 0;
    for (int k = 0; k < P; k++) {
        int ok = is_transformable(ss[k], ts[k], N);
        if (ok) yes++;
        check = mix(check, ok ? 1 : 0);
    }
    printf("40 problems of 100000 digits: %lld transformable, checksum %lld\n", (long long)yes, (long long)check);
    for (int k = 0; k < P; k++) {
        free(ss[k]);
        free(ts[k]);
    }
    return 0;
}
