// LeetCode #2282: Number of People That Can Be Seen in a Grid -- the
// bench, the ★ arm. The grid is one `m * n` block, and each line is read
// with a stride: 1 along a row, `n` down a column.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// adds to `seen[k * stride]` how many each person of a line of `len` sees
static void sightings(const int64_t *line, int64_t len, int64_t stride, int64_t *seen,
                      int64_t *stack) {
    int64_t top = 0;
    for (int64_t i = len - 1; i >= 0; i--) {
        int64_t h = line[i * stride];
        while (top > 0 && stack[top - 1] < h) {
            top--;
            seen[i * stride]++;
        }
        if (top > 0) {
            seen[i * stride]++;
            if (stack[top - 1] == h) top--;
        }
        stack[top++] = h;
    }
}

static void see_people(const int64_t *heights, int64_t m, int64_t n, int64_t *answer) {
    int64_t *stack = malloc((m > n ? m : n) * sizeof(int64_t));
    for (int64_t k = 0; k < m * n; k++) answer[k] = 0;
    for (int64_t i = 0; i < m; i++) sightings(heights + i * n, n, 1, answer + i * n, stack);
    for (int64_t j = 0; j < n; j++) sightings(heights + j, m, n, answer + j, stack);
    free(stack);
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2282;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    int64_t *heights = malloc(400 * 400 * sizeof(int64_t));
    int64_t *answer = malloc(400 * 400 * sizeof(int64_t));
    for (int t = 0; t < 40; t++) {
        for (int k = 0; k < 400 * 400; k++) {
            int64_t top = next_random();
            heights[k] = (top * 32768 + next_random()) % 100000 + 1;
        }
        see_people(heights, 400, 400, answer);
        int64_t seen = 0;
        for (int k = 0; k < 400 * 400; k++) seen += answer[k];
        check = (check * 31 + seen) % 1000000007;
    }
    free(heights);
    free(answer);
    printf("40 grids of 400 by 400: checksum %lld\n", (long long)check);
    return 0;
}
