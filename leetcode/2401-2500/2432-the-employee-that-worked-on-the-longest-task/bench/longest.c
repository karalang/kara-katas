// LeetCode #2432: The Employee That Worked on the Longest Task -- the
// bench, the ★ arm: one pass with the last leave time in hand, the best
// replaced by a longer task or an equal one of a smaller id.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t hardest_worker(int64_t n, int64_t **logs, int64_t m) {
    int64_t best_id = n, best_time = 0, start = 0;
    for (int64_t i = 0; i < m; i++) {
        int64_t time = logs[i][1] - start;
        if (time > best_time || (time == best_time && logs[i][0] < best_id)) {
            best_time = time;
            best_id = logs[i][0];
        }
        start = logs[i][1];
    }
    return best_id;
}

static int64_t seed = 2432;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 2000, m = 500;
    int64_t ***cases = malloc(count * sizeof(int64_t **));
    for (int c = 0; c < count; c++) {
        cases[c] = malloc(m * sizeof(int64_t *));
        int64_t time = 0, last = -1;
        for (int i = 0; i < m; i++) {
            int64_t id = next_random() % 500;
            if (id == last) id = (id + 1) % 500;
            time += 1 + next_random() % 3;
            cases[c][i] = malloc(2 * sizeof(int64_t));
            cases[c][i][0] = id;
            cases[c][i][1] = time;
            last = id;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++)
        for (int c = 0; c < count; c++) {
            cases[c][m - 1][1] += 1;
            check = (check * 31 + hardest_worker(500, cases[c], m) + p) % 1000000007;
        }
    printf("50 passes over 2000 cases of 500 logs: checksum %lld\n", (long long)check);
    for (int c = 0; c < count; c++) {
        for (int i = 0; i < m; i++) free(cases[c][i]);
        free(cases[c]);
    }
    free(cases);
    return 0;
}
