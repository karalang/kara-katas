// LeetCode #1632: Rank Transform of a Matrix -- the bench's C mirror: the
// ★ arm on 12 random 300 x 300 matrices of values 0 to 9999, all drawn
// first, with an open-addressing hash map written out for the per-value
// maps.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { COUNT = 12, R = 300, C = 300 };

typedef struct {
    int32_t value;
    int64_t r, c;
} Cell;

static int by_cell(const void *x, const void *y) {
    const Cell *a = x, *b = y;
    if (a->value != b->value) return a->value < b->value ? -1 : 1;
    if (a->r != b->r) return a->r < b->r ? -1 : 1;
    return (a->c > b->c) - (a->c < b->c);
}

// a map from int64 keys to int64 values, linear probing, fixed capacity
typedef struct {
    int64_t *keys, *values;
    char *used;
    size_t mask;
} Map;

static Map map_new(size_t entries) {
    size_t cap = 8;
    while (cap < 2 * entries) cap *= 2;
    Map m = {malloc(cap * sizeof(int64_t)), malloc(cap * sizeof(int64_t)), calloc(cap, 1), cap - 1};
    return m;
}

static void map_free(Map *m) {
    free(m->keys);
    free(m->values);
    free(m->used);
}

static size_t map_slot(const Map *m, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    size_t i = (size_t)(h >> 32) & m->mask;
    while (m->used[i] && m->keys[i] != key) i = (i + 1) & m->mask;
    return i;
}

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static void join_first(Map *first, int64_t line, int64_t id, int64_t *parent) {
    size_t s = map_slot(first, line);
    if (first->used[s]) {
        int64_t a = find(parent, id), b = find(parent, first->values[s]);
        parent[a] = b;
    } else {
        first->used[s] = 1;
        first->keys[s] = line;
        first->values[s] = id;
    }
}

static void matrix_rank_transform(int32_t (*matrix)[C], int32_t (*answer)[C]) {
    static Cell cells[R * C];
    static int64_t parent[R * C];
    int32_t row_max[R] = {0}, col_max[C] = {0};
    size_t n = 0;
    for (int64_t r = 0; r < R; r++)
        for (int64_t c = 0; c < C; c++) cells[n++] = (Cell){matrix[r][c], r, c};
    qsort(cells, n, sizeof(Cell), by_cell);
    for (int64_t i = 0; i < R * C; i++) parent[i] = i;
    size_t start = 0;
    while (start < n) {
        size_t end = start;
        while (end < n && cells[end].value == cells[start].value) end++;
        Map first_in_row = map_new(end - start), first_in_col = map_new(end - start);
        for (size_t k = start; k < end; k++) {
            int64_t id = cells[k].r * C + cells[k].c;
            join_first(&first_in_row, cells[k].r, id, parent);
            join_first(&first_in_col, cells[k].c, id, parent);
        }
        Map group_rank = map_new(end - start);
        for (size_t k = start; k < end; k++) {
            int64_t root = find(parent, cells[k].r * C + cells[k].c);
            int32_t a = row_max[cells[k].r], b = col_max[cells[k].c];
            int64_t rank = (a > b ? a : b) + 1;
            size_t s = map_slot(&group_rank, root);
            if (!group_rank.used[s]) {
                group_rank.used[s] = 1;
                group_rank.keys[s] = root;
                group_rank.values[s] = 0;
            }
            if (rank > group_rank.values[s]) group_rank.values[s] = rank;
        }
        for (size_t k = start; k < end; k++) {
            int64_t root = find(parent, cells[k].r * C + cells[k].c);
            int32_t rank = (int32_t)group_rank.values[map_slot(&group_rank, root)];
            answer[cells[k].r][cells[k].c] = rank;
            row_max[cells[k].r] = rank;
            col_max[cells[k].c] = rank;
        }
        map_free(&first_in_row);
        map_free(&first_in_col);
        map_free(&group_rank);
        start = end;
    }
}

static int64_t seed = 1632;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t matrices[COUNT][R][C], answer[R][C];
    for (int m = 0; m < COUNT; m++)
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) matrices[m][r][c] = (int32_t)(next_random() % 10000);
    int64_t check = 0, total = 0;
    for (int m = 0; m < COUNT; m++) {
        matrix_rank_transform(matrices[m], answer);
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) {
                total += answer[r][c];
                check = (check * 31 + answer[r][c]) % 1000000007;
            }
    }
    printf("12 matrices of 300 x 300: ranks sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
