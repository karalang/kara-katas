// Benchmark for #502: C mirror of the ★ arm (projects sorted by capital,
// profits in a heap); see ipo.kara. The project indices are sorted by
// capital with qsort, and the ready profits sit in a hand-written
// largest-first binary heap, fresh for each case, as the ★ arm's are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t *sort_capital;

static int by_capital(const void *a, const void *b) {
    int64_t x = sort_capital[*(const int64_t *)a], y = sort_capital[*(const int64_t *)b];
    return (x > y) - (x < y);
}

static int64_t find_maximized_capital(int64_t k, int64_t w, const int64_t *profits,
                                      const int64_t *capital, int64_t n) {
    int64_t *order = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) order[i] = i;
    sort_capital = capital;
    qsort(order, n, sizeof(int64_t), by_capital);
    int64_t *heap = malloc(n * sizeof(int64_t));
    int64_t size = 0, money = w, next = 0;
    for (int64_t round = 0; round < k; round++) {
        while (next < n && capital[order[next]] <= money) {
            int64_t v = profits[order[next]], i = size++;
            while (i > 0 && heap[(i - 1) / 2] < v) {
                heap[i] = heap[(i - 1) / 2];
                i = (i - 1) / 2;
            }
            heap[i] = v;
            next++;
        }
        if (size == 0) break;
        money += heap[0];
        int64_t last = heap[--size], i = 0;
        for (;;) {
            int64_t c = 2 * i + 1;
            if (c >= size) break;
            if (c + 1 < size && heap[c + 1] > heap[c]) c++;
            if (heap[c] <= last) break;
            heap[i] = heap[c];
            i = c;
        }
        heap[i] = last;
    }
    free(order);
    free(heap);
    return money;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 60 cases of 100,000 projects with k = 100,000, profits 0 to 10,000
    // and capital needs from 0 to 10^5, 10^7 or 10^9 in turn, w from 0
    // to 1,000; built once. Then each case is solved once.
    int64_t cases = 60, n = 100000, seed = 502;
    int64_t *profits = malloc(cases * n * sizeof(int64_t));
    int64_t *capital = malloc(cases * n * sizeof(int64_t));
    int64_t *starts = malloc(cases * sizeof(int64_t));
    for (int64_t c = 0; c < cases; c++) {
        int64_t scale = c % 3 == 0 ? 100001 : c % 3 == 1 ? 10000001 : 1000000001;
        for (int64_t i = 0; i < n; i++) {
            profits[c * n + i] = next_random(&seed) % 10001;
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            capital[c * n + i] = (hi * 32768 + lo) % scale;
        }
        starts[c] = next_random(&seed) % 1001;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t c = 0; c < cases; c++) {
        int64_t got = find_maximized_capital(n, starts[c], profits + c * n, capital + c * n, n);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    printf("%lld cases of %lld projects: total capital %lld, checksum %lld\n",
           (long long)cases, (long long)n, (long long)total, (long long)checksum);
    return 0;
}
