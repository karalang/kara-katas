// LeetCode #1476: Subrectangle Queries -- bench, C mirror of
// subrectangle_queries.kara. The grid is 100 rows, each its own malloc'ed
// array, as the Kāra and Rust grids are a list of lists.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int32_t **rect;
} SubrectangleQueries;

static void update_subrectangle(SubrectangleQueries *q, int32_t row1, int32_t col1, int32_t row2, int32_t col2,
                                int32_t new_value) {
    for (int32_t r = row1; r <= row2; r++) {
        for (int32_t c = col1; c <= col2; c++) {
            q->rect[r][c] = new_value;
        }
    }
}

static int32_t get_value(const SubrectangleQueries *q, int32_t row, int32_t col) {
    return q->rect[row][col];
}

static int64_t seed = 1476;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    SubrectangleQueries q;
    q.rect = malloc(sizeof(int32_t *) * 100);
    for (int r = 0; r < 100; r++) {
        q.rect[r] = malloc(sizeof(int32_t) * 100);
        for (int c = 0; c < 100; c++) {
            int64_t hi = next_random();
            q.rect[r][c] = (int32_t)(1 + (hi * 32768 + next_random()) % 1000000000);
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 5000; pass++) {
        for (int k = 0; k < 250; k++) {
            int64_t r1 = next_random() % 100;
            int64_t r2 = r1 + next_random() % (100 - r1);
            int64_t c1 = next_random() % 100;
            int64_t c2 = c1 + next_random() % (100 - c1);
            update_subrectangle(&q, (int32_t)r1, (int32_t)c1, (int32_t)r2, (int32_t)c2,
                                (int32_t)(1 + check % 1000000000));
            int64_t r = next_random() % 100;
            int64_t c = next_random() % 100;
            check = (check * 31 + get_value(&q, (int32_t)r, (int32_t)c) + pass) % 1000000007;
        }
    }
    printf("5000 passes of 250 updates on 100 by 100: checksum %lld\n", (long long)check);
    for (int r = 0; r < 100; r++) free(q.rect[r]);
    free(q.rect);
    return 0;
}
