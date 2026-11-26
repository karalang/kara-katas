// LeetCode #1418: the bench in C, mirroring display_table.kara. C has no
// ordered map: the dishes in an open-addressing hash table, then sorted,
// and each table's counts in a row indexed by table number.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *guest, *table, *food;
} Order;

typedef struct {
    char ***cells;  // rows of cells, each a malloc'd string
    int64_t rows, cols;
} Table;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static char *copy(const char *s) {
    size_t n = strlen(s) + 1;
    char *c = malloc(n);
    memcpy(c, s, n);
    return c;
}

static char *number(int64_t x) {
    char buf[24];
    snprintf(buf, sizeof buf, "%lld", (long long)x);
    return copy(buf);
}

static int cmp_str(const void *a, const void *b) {
    return strcmp(*(char *const *)a, *(char *const *)b);
}

static Table display_table(const Order *orders, int64_t n) {
    int64_t cap = 64;
    char **slot = calloc(cap, sizeof(char *));
    int64_t *slot_id = calloc(cap, sizeof(int64_t));
    char **foods = NULL;
    int64_t nfoods = 0;
    int64_t *ids = malloc(n * sizeof(int64_t));
    int64_t *tables = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        if (2 * (nfoods + 1) > cap) {
            int64_t ncap = cap * 2;
            char **ns = calloc(ncap, sizeof(char *));
            int64_t *ni = calloc(ncap, sizeof(int64_t));
            for (int64_t k = 0; k < cap; k++)
                if (slot[k]) {
                    uint64_t h = hash(slot[k]) & (ncap - 1);
                    while (ns[h]) h = (h + 1) & (ncap - 1);
                    ns[h] = slot[k];
                    ni[h] = slot_id[k];
                }
            free(slot);
            free(slot_id);
            slot = ns;
            slot_id = ni;
            cap = ncap;
        }
        uint64_t h = hash(orders[i].food) & (cap - 1);
        while (slot[h] && strcmp(slot[h], orders[i].food) != 0) h = (h + 1) & (cap - 1);
        if (!slot[h]) {
            slot[h] = orders[i].food;
            slot_id[h] = nfoods;
            foods = realloc(foods, (nfoods + 1) * sizeof(char *));
            foods[nfoods++] = orders[i].food;
        }
        ids[i] = slot_id[h];
        tables[i] = atoll(orders[i].table);
    }
    // each dish's column once the dishes are sorted
    char **sorted = malloc(nfoods * sizeof(char *));
    memcpy(sorted, foods, nfoods * sizeof(char *));
    qsort(sorted, nfoods, sizeof(char *), cmp_str);
    int64_t *column = malloc(nfoods * sizeof(int64_t));
    for (int64_t c = 0; c < nfoods; c++) {
        uint64_t h = hash(sorted[c]) & (cap - 1);
        while (strcmp(slot[h], sorted[c]) != 0) h = (h + 1) & (cap - 1);
        column[slot_id[h]] = c;
    }
    int64_t *counts = calloc(501 * nfoods, sizeof(int64_t));
    char seen[501] = {0};
    for (int64_t i = 0; i < n; i++) {
        counts[tables[i] * nfoods + column[ids[i]]]++;
        seen[tables[i]] = 1;
    }
    int64_t rows = 1;
    for (int t = 1; t <= 500; t++) rows += seen[t];
    Table out = {malloc(rows * sizeof(char **)), rows, nfoods + 1};
    out.cells[0] = malloc((nfoods + 1) * sizeof(char *));
    out.cells[0][0] = copy("Table");
    for (int64_t c = 0; c < nfoods; c++) out.cells[0][c + 1] = copy(sorted[c]);
    int64_t r = 1;
    for (int t = 1; t <= 500; t++) {
        if (!seen[t]) continue;
        out.cells[r] = malloc((nfoods + 1) * sizeof(char *));
        out.cells[r][0] = number(t);
        for (int64_t c = 0; c < nfoods; c++) out.cells[r][c + 1] = number(counts[t * nfoods + c]);
        r++;
    }
    free(slot);
    free(slot_id);
    free(foods);
    free(ids);
    free(tables);
    free(sorted);
    free(column);
    free(counts);
    return out;
}

static int64_t seed = 1418;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    char *dishes[30];
    for (int i = 0; i < 30; i++) {
        int64_t n = 1 + next_random() % 20;
        dishes[i] = malloc(n + 1);
        for (int64_t j = 0; j < n; j++) {
            int64_t r = next_random();
            dishes[i][j] = r % 6 == 0 ? ' ' : letters[r / 6 % 52];
        }
        dishes[i][n] = 0;
    }
    Order *pool = malloc(200000 * sizeof(Order));
    for (int i = 0; i < 200000; i++) {
        int64_t r = next_random();
        char buf[24];
        snprintf(buf, sizeof buf, "guest%lld", (long long)(r % 100));
        pool[i].guest = copy(buf);
        pool[i].table = number(1 + r / 100 % 500);
        pool[i].food = copy(dishes[next_random() % 30]);
    }
    int64_t check = 0;
    for (int w = 0; w < 100; w++) {
        int64_t start = next_random() % 150001;
        Table t = display_table(pool + start, 50000);
        for (int64_t r = 0; r < t.rows; r++) {
            for (int64_t c = 0; c < t.cols; c++) {
                for (const char *p = t.cells[r][c]; *p; p++) check = (check * 131 + (unsigned char)*p) % 1000000007;
                check = (check * 131 + 7) % 1000000007;
                free(t.cells[r][c]);
            }
            free(t.cells[r]);
        }
        free(t.cells);
    }
    printf("100 windows of 5 * 10^4 orders: checksum %lld\n", (long long)check);
    return 0;
}
