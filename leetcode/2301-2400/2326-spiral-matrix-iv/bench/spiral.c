// LeetCode #2326: Spiral Matrix IV -- the bench, the ★ arm in C. A walker
// starts at the top left heading right and writes the list's values one
// by one, turning clockwise when the next cell is off the grid or already
// written. O(m n). The grid is an array of row pointers, as the others'
// is a list of rows.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static int64_t **spiral_matrix(int64_t m, int64_t n, const ListNode *head) {
    int64_t **grid = malloc(m * sizeof(int64_t *));
    for (int64_t i = 0; i < m; i++) {
        grid[i] = malloc(n * sizeof(int64_t));
        for (int64_t j = 0; j < n; j++)
            grid[i][j] = -1;
    }
    static const int64_t moves[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
    int64_t r = 0, c = 0, d = 0;
    for (const ListNode *node = head; node; node = node->next) {
        grid[r][c] = node->val;
        int64_t nr = r + moves[d][0], nc = c + moves[d][1];
        if (nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr][nc] != -1)
            d = (d + 1) % 4;
        r += moves[d][0];
        c += moves[d][1];
    }
    return grid;
}

static int64_t seed = 2326;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rows[10] = {100, 200, 250, 400, 500, 1000, 50, 125, 80, 160};
    ListNode *heads[10];
    for (int k = 0; k < 10; k++) {
        ListNode *head = NULL;
        for (int i = 0; i < 90000 + 1111 * k; i++) {
            ListNode *node = malloc(sizeof(ListNode));
            node->val = next_random() % 1001;
            node->next = head;
            head = node;
        }
        heads[k] = head;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 30; p++)
        for (int64_t k = 0; k < 10; k++) {
            int64_t m = rows[(p + k) % 10];
            int64_t n = 100000 / m;
            int64_t **grid = spiral_matrix(m, n, heads[k]);
            check = (check * 31 + grid[p % m][(3 * p + k) % n] + grid[m / 2][n / 2] + 2) % 1000000007;
            for (int64_t i = 0; i < m; i++)
                free(grid[i]);
            free(grid);
        }
    printf("30 passes over 10 lists in grids of 10^5 cells: checksum %lld\n", (long long)check);
    for (int k = 0; k < 10; k++)
        while (heads[k]) {
            ListNode *next = heads[k]->next;
            free(heads[k]);
            heads[k] = next;
        }
    return 0;
}
