// LeetCode #694: Number of Distinct Islands -- bench program, C mirror of the union-find arm.
#include <stdio.h>
#include <stdlib.h>

#define M 50
#define N 50

static long long seed = 694;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct { long long *cells; int len, cap; } Shape;

static int find(int *parent, int x) {
    int root = x;
    while (parent[root] != root) root = parent[root];
    while (parent[x] != root) {
        int next = parent[x];
        parent[x] = root;
        x = next;
    }
    return root;
}

// Lexicographic, a shorter prefix first, as Vec[i64] compares.
static int by_cells(const void *pa, const void *pb) {
    const Shape *a = pa, *b = pb;
    for (int i = 0; i < a->len && i < b->len; i++)
        if (a->cells[i] != b->cells[i]) return a->cells[i] < b->cells[i] ? -1 : 1;
    return (a->len > b->len) - (a->len < b->len);
}

static int same(const Shape *a, const Shape *b) { return by_cells(a, b) == 0; }

static long long num_distinct_islands(int grid[M][N]) {
    int *parent = malloc(sizeof(int) * M * N);
    for (int i = 0; i < M * N; i++) parent[i] = i;
    for (int r = 0; r < M; r++)
        for (int c = 0; c < N; c++) {
            if (!grid[r][c]) continue;
            if (r + 1 < M && grid[r + 1][c]) parent[find(parent, r * N + c)] = find(parent, (r + 1) * N + c);
            if (c + 1 < N && grid[r][c + 1]) parent[find(parent, r * N + c)] = find(parent, r * N + c + 1);
        }
    int *first = malloc(sizeof(int) * M * N), *slot = malloc(sizeof(int) * M * N);
    for (int i = 0; i < M * N; i++) first[i] = slot[i] = -1;
    Shape *shapes = malloc(sizeof(Shape) * M * N);
    int count = 0;
    for (int r = 0; r < M; r++)
        for (int c = 0; c < N; c++) {
            if (!grid[r][c]) continue;
            int root = find(parent, r * N + c);
            if (first[root] < 0) {
                first[root] = r * N + c;
                slot[root] = count;
                shapes[count++] = (Shape){malloc(sizeof(long long) * 4), 0, 4};
            }
            Shape *s = &shapes[slot[root]];
            if (s->len == s->cap) s->cells = realloc(s->cells, sizeof(long long) * (s->cap *= 2));
            s->cells[s->len++] = (long long)(r - first[root] / N) * 200 + (c - first[root] % N);
        }
    qsort(shapes, count, sizeof(Shape), by_cells);
    long long distinct = 0;
    for (int i = 0; i < count; i++)
        if (i == 0 || !same(&shapes[i], &shapes[i - 1])) distinct++;
    for (int i = 0; i < count; i++) free(shapes[i].cells);
    free(shapes);
    free(first);
    free(slot);
    free(parent);
    return distinct;
}

int main(void) {
    static int grids[40][M][N];
    for (int g = 0; g < 40; g++) {
        long long percent = 30 + next_random() % 31;
        for (int r = 0; r < M; r++)
            for (int c = 0; c < N; c++) grids[g][r][c] = next_random() % 100 < percent;
    }
    int rounds = 150;
    long long total = 0, checksum = 0;
    for (int k = 0; k < rounds; k++)
        for (int g = 0; g < 40; g++) {
            long long r = num_distinct_islands(grids[g]);
            total += r;
            checksum = (checksum * 31 + r) % 1000000007;
        }
    printf("%d rounds of 40 grids of 50 by 50: %lld distinct islands counted, checksum %lld\n", rounds, total, checksum);
    return 0;
}
