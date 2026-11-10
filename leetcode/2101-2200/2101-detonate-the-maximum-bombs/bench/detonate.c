// LeetCode #2101: Detonate the Maximum Bombs -- C mirror of the ★ arm's
// benchmark (detonate.kara): the same 2000 fields of 100 bombs, adjacency
// lists (fixed rows of at most 100) and a breadth-first search from each
// bomb with an array as the queue.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { N = 100 };

static int64_t maximum_detonation(int64_t bombs[][3], int n) {
    static int reach[N][N];
    int degree[N] = {0};
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            int64_t dx = bombs[i][0] - bombs[j][0], dy = bombs[i][1] - bombs[j][1];
            if (i != j && dx * dx + dy * dy <= bombs[i][2] * bombs[i][2]) reach[i][degree[i]++] = j;
        }
    int64_t best = 0;
    for (int start = 0; start < n; start++) {
        char seen[N];
        int queue[N], head = 0, tail = 0;
        memset(seen, 0, sizeof seen);
        seen[start] = 1;
        queue[tail++] = start;
        int64_t count = 0;
        while (head < tail) {
            int i = queue[head++];
            count++;
            for (int k = 0; k < degree[i]; k++) {
                int j = reach[i][k];
                if (!seen[j]) {
                    seen[j] = 1;
                    queue[tail++] = j;
                }
            }
        }
        if (count > best) best = count;
    }
    return best;
}

static int64_t seed = 2101;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int f = 0; f < 2000; f++) {
        int64_t bombs[N][3];
        for (int i = 0; i < N; i++) {
            bombs[i][0] = next_random() % 1000 + 1;
            bombs[i][1] = next_random() % 1000 + 1;
            bombs[i][2] = next_random() % 150 + 1;
        }
        int64_t got = maximum_detonation(bombs, N);
        total += got;
        check = (check * 31 + got) % 1000000007;
    }
    printf("2000 fields: %lld bombs in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
