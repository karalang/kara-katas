// Benchmark for #655: each node placed from its parent, as the Kara ★
// arm. Empty cells point at one shared "", as an empty Kara `String`
// allocates nothing; each value is formatted into its own allocation.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static char empty[] = "";

static int64_t height(TreeNode *node) {
    if (!node) return 0;
    int64_t l = height(node->left), r = height(node->right);
    return 1 + (l > r ? l : r);
}

static void place(TreeNode *node, int64_t row, int64_t column, int64_t h, char ***grid) {
    if (!node) return;
    char buf[24];
    int len = snprintf(buf, sizeof buf, "%lld", (long long)node->val);
    char *s = malloc(len + 1);
    memcpy(s, buf, len + 1);
    grid[row][column] = s;
    if (row < h) {
        int64_t step = (int64_t)1 << (h - row - 1);
        place(node->left, row + 1, column - step, h, grid);
        place(node->right, row + 1, column + step, h, grid);
    }
}

static char ***print_tree(TreeNode *root, int64_t *rows, int64_t *columns) {
    int64_t h = height(root) - 1;
    *rows = h + 1;
    *columns = ((int64_t)1 << (h + 1)) - 1;
    char ***grid = malloc(*rows * sizeof *grid);
    for (int64_t r = 0; r < *rows; r++) {
        grid[r] = malloc(*columns * sizeof **grid);
        for (int64_t c = 0; c < *columns; c++) grid[r][c] = empty;
    }
    place(root, 0, (*columns - 1) / 2, h, grid);
    return grid;
}

static int64_t seed = 655;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static TreeNode *random_tree(int64_t levels, int64_t chance) {
    if (levels == 0) return NULL;
    TreeNode *n = malloc(sizeof *n);
    n->val = next_random() % 199 - 99;
    n->left = n->right = NULL;
    if (next_random() % 100 < chance) n->left = random_tree(levels - 1, chance);
    if (next_random() % 100 < chance) n->right = random_tree(levels - 1, chance);
    return n;
}

static void release(TreeNode *node) {
    if (!node) return;
    release(node->left);
    release(node->right);
    free(node);
}

int main(void) {
    int inputs = 8, rounds = 10000;
    TreeNode *trees[8];
    for (int i = 0; i < inputs; i++) trees[i] = random_tree(10, 85);
    int64_t cells = 0, checksum = 0;
    for (int r = 0; r < rounds; r++) {
        int64_t rows, columns;
        char ***grid = print_tree(trees[(r * 3) % inputs], &rows, &columns);
        int64_t filled = 0, chars = 0;
        for (int64_t i = 0; i < rows; i++) {
            for (int64_t c = 0; c < columns; c++) {
                size_t len = strlen(grid[i][c]);
                if (len > 0) {
                    filled++;
                    chars += len;
                    free(grid[i][c]);
                }
            }
            free(grid[i]);
        }
        free(grid);
        cells += rows * columns;
        checksum = (checksum * 31 + filled * 1000 + chars) % 1000000007;
    }
    for (int i = 0; i < inputs; i++) release(trees[i]);
    printf("%d trees, %d rounds: %lld cells, checksum %lld\n", inputs, rounds, (long long)cells,
           (long long)checksum);
    return 0;
}
