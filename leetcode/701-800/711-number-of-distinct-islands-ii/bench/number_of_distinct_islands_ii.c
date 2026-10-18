// LeetCode #711: Number of Distinct Islands II -- canonical forms
// counted by sorting.
// Benchmark mirror of the Kara sorted arm: each island by depth-first
// search with a stack; its canonical form the smallest of its eight
// symmetries, sorted and moved to the origin; forms sorted and counted.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t r, c;
} Cell;

typedef struct {
    int64_t *v;
    int64_t len;
} Form;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int cmp_cell(const void *a, const void *b) {
    const Cell *x = a, *y = b;
    if (x->r != y->r) return x->r < y->r ? -1 : 1;
    if (x->c != y->c) return x->c < y->c ? -1 : 1;
    return 0;
}

static int cmp_flat(const int64_t *a, int64_t na, const int64_t *b,
                    int64_t nb) {
    int64_t n = na < nb ? na : nb;
    for (int64_t i = 0; i < n; i++) {
        if (a[i] != b[i]) return a[i] < b[i] ? -1 : 1;
    }
    return (na > nb) - (na < nb);
}

static int cmp_form(const void *a, const void *b) {
    const Form *x = a, *y = b;
    return cmp_flat(x->v, x->len, y->v, y->len);
}

static Form canonical(const Cell *cells, int64_t n) {
    Cell *moved = malloc(n * sizeof(Cell));
    int64_t *flat = malloc(2 * n * sizeof(int64_t));
    int64_t *best = malloc(2 * n * sizeof(int64_t));
    for (int k = 0; k < 8; k++) {
        for (int64_t i = 0; i < n; i++) {
            int64_t a = k < 4 ? cells[i].r : cells[i].c;
            int64_t b = k < 4 ? cells[i].c : cells[i].r;
            moved[i].r = k % 2 == 1 ? -a : a;
            moved[i].c = k % 4 >= 2 ? -b : b;
        }
        qsort(moved, n, sizeof(Cell), cmp_cell);
        int64_t r0 = moved[0].r, c0 = moved[0].c;
        for (int64_t i = 0; i < n; i++) {
            flat[2 * i] = moved[i].r - r0;
            flat[2 * i + 1] = moved[i].c - c0;
        }
        if (k == 0 || cmp_flat(flat, 2 * n, best, 2 * n) < 0) {
            memcpy(best, flat, 2 * n * sizeof(int64_t));
        }
    }
    free(moved);
    free(flat);
    return (Form){best, 2 * n};
}

static int64_t num_distinct_islands2(int64_t **grid, int64_t rows,
                                     int64_t cols) {
    char *seen = calloc(rows * cols, 1);
    Form *forms = malloc(rows * cols * sizeof(Form));
    int64_t nforms = 0;
    Cell *cells = malloc(rows * cols * sizeof(Cell));
    int64_t *stack = malloc(rows * cols * sizeof(int64_t));
    for (int64_t start = 0; start < rows * cols; start++) {
        if (grid[start / cols][start % cols] == 0 || seen[start]) continue;
        int64_t ncells = 0, top = 0;
        stack[top++] = start;
        seen[start] = 1;
        while (top > 0) {
            int64_t at = stack[--top];
            int64_t r = at / cols, c = at % cols;
            cells[ncells++] = (Cell){r, c};
            if (r > 0 && grid[r - 1][c] == 1 && !seen[at - cols]) {
                seen[at - cols] = 1;
                stack[top++] = at - cols;
            }
            if (r + 1 < rows && grid[r + 1][c] == 1 && !seen[at + cols]) {
                seen[at + cols] = 1;
                stack[top++] = at + cols;
            }
            if (c > 0 && grid[r][c - 1] == 1 && !seen[at - 1]) {
                seen[at - 1] = 1;
                stack[top++] = at - 1;
            }
            if (c + 1 < cols && grid[r][c + 1] == 1 && !seen[at + 1]) {
                seen[at + 1] = 1;
                stack[top++] = at + 1;
            }
        }
        forms[nforms++] = canonical(cells, ncells);
    }
    qsort(forms, nforms, sizeof(Form), cmp_form);
    int64_t count = 0;
    for (int64_t i = 0; i < nforms; i++) {
        if (i == 0 || cmp_form(&forms[i], &forms[i - 1]) != 0) count++;
    }
    for (int64_t i = 0; i < nforms; i++) free(forms[i].v);
    free(forms);
    free(cells);
    free(stack);
    free(seen);
    return count;
}

int main(void) {
    int64_t seed = 711;
    enum { G = 100, N = 50 };
    int64_t **grids[G];
    for (int g = 0; g < G; g++) {
        int64_t pct = 30 + g * 2 / 5;
        grids[g] = malloc(N * sizeof(int64_t *));
        for (int r = 0; r < N; r++) {
            grids[g][r] = malloc(N * sizeof(int64_t));
            for (int c = 0; c < N; c++) {
                grids[g][r][c] = next_random(&seed) % 100 < pct ? 1 : 0;
            }
        }
    }
    int64_t sum = 0;
    for (int round = 0; round < 10; round++) {
        for (int g = 0; g < G; g++) {
            sum += num_distinct_islands2(grids[g], N, N);
        }
    }
    for (int g = 0; g < G; g++) {
        for (int r = 0; r < N; r++) free(grids[g][r]);
        free(grids[g]);
    }
    printf("10 rounds of 100 grids of 50 by 50: %lld distinct islands\n", (long long)sum);
    return 0;
}
