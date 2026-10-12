// Benchmark for #401: mirror of binary_watch.kara (try every time). Each
// time is a heap-allocated string, as in the other mirrors, collected into a
// growable array that is freed after each call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t ones(int64_t x) {
    int64_t count = 0, y = x;
    while (y > 0) {
        count += y % 2;
        y = y / 2;
    }
    return count;
}

typedef struct {
    char **items;
    int64_t len, cap;
} List;

static void push(List *l, char *s) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof(char *));
    }
    l->items[l->len++] = s;
}

static List read_binary_watch(int64_t turned_on) {
    List times = {0};
    for (int64_t h = 0; h < 12; h++) {
        for (int64_t m = 0; m < 60; m++) {
            if (ones(h) + ones(m) == turned_on) {
                char buf[8];
                snprintf(buf, sizeof buf, "%lld:%02lld", (long long)h, (long long)m);
                push(&times, strdup(buf));
            }
        }
    }
    return times;
}

int main(int argc, char **argv) {
    int64_t calls = argc > 1 ? atoll(argv[1]) : 50000;
    int64_t times_total = 0, chars = 0;
    for (int64_t c = 0; c < calls; c++) {
        List times = read_binary_watch(c % 11);
        times_total += times.len;
        for (int64_t i = 0; i < times.len; i++) {
            chars += (int64_t)strlen(times.items[i]);
            free(times.items[i]);
        }
        free(times.items);
    }
    printf("%lld calls: %lld times, %lld characters\n", (long long)calls, (long long)times_total, (long long)chars);
    return 0;
}
