// Benchmark for #675: a breadth-first search for each walk, as the Kara
// ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 675;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t steps(const int64_t *forest, int64_t rows, int64_t cols, int64_t sr, int64_t sc,
                     int64_t tr, int64_t tc) {
    if (sr == tr && sc == tc) return 0;
    char *seen = calloc(rows * cols, 1);
    int64_t *queue = malloc(sizeof(int64_t) * rows * cols);
    int64_t found = -1;
    static const int64_t dr[4] = {-1, 1, 0, 0};
    static const int64_t dc[4] = {0, 0, -1, 1};
    int64_t len = 0;
    queue[len++] = sr * cols + sc;
    seen[sr * cols + sc] = 1;
    int64_t head = 0;
    int64_t dist = 0;
    while (head < len && found < 0) {
        int64_t end = len;
        dist += 1;
        while (head < end && found < 0) {
            int64_t cell = queue[head++];
            int64_t r = cell / cols;
            int64_t c = cell % cols;
            for (int k = 0; k < 4; k++) {
                int64_t nr = r + dr[k];
                int64_t nc = c + dc[k];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && forest[nr * cols + nc] != 0 &&
                    !seen[nr * cols + nc]) {
                    if (nr == tr && nc == tc) {
                        found = dist;
                        break;
                    }
                    seen[nr * cols + nc] = 1;
                    queue[len++] = nr * cols + nc;
                }
            }
        }
    }
    free(seen);
    free(queue);
    return found;
}

typedef struct {
    int64_t height, r, c;
} Tree;

static int by_height(const void *a, const void *b) {
    int64_t x = ((const Tree *)a)->height;
    int64_t y = ((const Tree *)b)->height;
    return (x > y) - (x < y);
}

static int64_t cut_off_tree(const int64_t *forest, int64_t rows, int64_t cols) {
    Tree *trees = malloc(sizeof(Tree) * rows * cols);
    int64_t count = 0;
    for (int64_t r = 0; r < rows; r++) {
        for (int64_t c = 0; c < cols; c++) {
            if (forest[r * cols + c] > 1) {
                trees[count].height = forest[r * cols + c];
                trees[count].r = r;
                trees[count].c = c;
                count++;
            }
        }
    }
    qsort(trees, count, sizeof(Tree), by_height);
    int64_t total = 0;
    int64_t r = 0;
    int64_t c = 0;
    for (int64_t k = 0; k < count; k++) {
        int64_t d = steps(forest, rows, cols, r, c, trees[k].r, trees[k].c);
        if (d < 0) {
            total = -1;
            break;
        }
        total += d;
        r = trees[k].r;
        c = trees[k].c;
    }
    free(trees);
    return total;
}

static int64_t *random_forest(int64_t rows, int64_t cols, int64_t walls, int64_t trees) {
    int64_t *forest = malloc(sizeof(int64_t) * rows * cols);
    int64_t *spots = malloc(sizeof(int64_t) * rows * cols);
    int64_t n = 0;
    for (int64_t r = 0; r < rows; r++) {
        for (int64_t c = 0; c < cols; c++) {
            int64_t k = next_random() % 100;
            if ((r > 0 || c > 0) && k < walls) {
                forest[r * cols + c] = 0;
            } else {
                forest[r * cols + c] = 1;
                if (k < walls + trees) spots[n++] = r * cols + c;
            }
        }
    }
    int64_t i = n;
    while (i > 1) {
        int64_t j = next_random() % i;
        i -= 1;
        int64_t t = spots[i];
        spots[i] = spots[j];
        spots[j] = t;
    }
    for (int64_t k = 0; k < n; k++) forest[spots[k]] = 2 + k * 7;
    free(spots);
    return forest;
}

int main(void) {
    int64_t forests = 40;
    int64_t sum = 0;
    int64_t reached = 0;
    for (int64_t f = 0; f < forests; f++) {
        int64_t *forest = random_forest(50, 50, 10, 30);
        int64_t got = cut_off_tree(forest, 50, 50);
        if (got >= 0) reached += 1;
        sum = (sum * 31 + got + 1) % 1000000007;
        free(forest);
    }
    printf("%lld forests of 50x50, %lld reachable: checksum %lld\n", (long long)forests,
           (long long)reached, (long long)sum);
    return 0;
}
