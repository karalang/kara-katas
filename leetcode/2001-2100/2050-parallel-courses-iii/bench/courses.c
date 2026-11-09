// LeetCode #2050: Parallel Courses III -- C mirror of the ★ arm's
// benchmark (courses.kara): the same 40 graphs of 50000 courses, the same
// Kahn's topological order. Each course's dependents are a growable array,
// as a `Vec` is, and the queue a ring buffer as large as the courses.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} List;

static void push(List *l, int64_t x) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = x;
}

static int64_t seed = 2050;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t minimum_time(int64_t n, const int64_t *ra, const int64_t *rb, int64_t m, const int64_t *time) {
    List *next = calloc(n, sizeof(List));
    int64_t *waiting = calloc(n, sizeof(int64_t));
    for (int64_t k = 0; k < m; k++) {
        push(&next[ra[k] - 1], rb[k] - 1);
        waiting[rb[k] - 1]++;
    }
    int64_t *start = calloc(n, sizeof(int64_t));
    int64_t *queue = malloc(n * sizeof(int64_t));
    int64_t head = 0, tail = 0;
    for (int64_t v = 0; v < n; v++)
        if (waiting[v] == 0) queue[tail++] = v;
    int64_t months = 0;
    while (head < tail) {
        int64_t v = queue[head++];
        int64_t done = start[v] + time[v];
        if (done > months) months = done;
        for (int64_t k = 0; k < next[v].len; k++) {
            int64_t w = next[v].items[k];
            if (done > start[w]) start[w] = done;
            if (--waiting[w] == 0) queue[tail++] = w;
        }
    }
    for (int64_t v = 0; v < n; v++) free(next[v].items);
    free(next);
    free(waiting);
    free(start);
    free(queue);
    return months;
}

int main(void) {
    int64_t n = 50000, sum = 0, check = 0;
    int64_t *order = malloc(n * sizeof(int64_t));
    int64_t *ra = malloc(n * sizeof(int64_t)), *rb = malloc(n * sizeof(int64_t));
    int64_t *time = malloc(n * sizeof(int64_t));
    for (int64_t t = 0; t < 40; t++) {
        int64_t reach = 1 + t * 1000;
        for (int64_t i = 0; i < n; i++) order[i] = i + 1;
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t x = order[i];
            order[i] = order[j];
            order[j] = x;
        }
        for (int64_t i = 1; i < n; i++) {
            int64_t span = reach < i ? reach : i;
            int64_t at = i - (next_random() % span + 1);
            ra[i - 1] = order[at];
            rb[i - 1] = order[i];
        }
        for (int64_t v = 0; v < n; v++) time[v] = next_random() % 10000 + 1;
        int64_t months = minimum_time(n, ra, rb, n - 1, time);
        sum += months;
        check = (check * 31 + months) % 1000000007;
    }
    free(order);
    free(ra);
    free(rb);
    free(time);
    printf("40 graphs: sum %lld, checksum %lld\n", (long long)sum, (long long)check);
    return 0;
}
