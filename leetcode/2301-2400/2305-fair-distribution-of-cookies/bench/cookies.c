// LeetCode #2305: Fair Distribution of Cookies -- the bench, the ★ arm in
// C. Backtrack each bag over the children whose load stays under the
// best so far, trying only the first child with nothing yet.
#include <stdint.h>
#include <stdio.h>

enum { LISTS = 2000, BAGS = 8 };

static void place(const int64_t *cookies, int i, int64_t *loads, int k, int64_t *best) {
    if (i == BAGS) {
        int64_t most = loads[0];
        for (int c = 1; c < k; c++)
            if (loads[c] > most) most = loads[c];
        if (most < *best) *best = most;
        return;
    }
    for (int c = 0; c < k; c++) {
        if (loads[c] + cookies[i] < *best) {
            loads[c] += cookies[i];
            place(cookies, i + 1, loads, k, best);
            loads[c] -= cookies[i];
        }
        if (loads[c] == 0) break;
    }
}

static int64_t distribute_cookies(const int64_t *cookies, int k) {
    int64_t loads[BAGS] = {0};
    int64_t best = INT64_MAX;
    place(cookies, 0, loads, k, &best);
    return best;
}

static int64_t seed = 2305;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t lists[LISTS][BAGS];
    for (int a = 0; a < LISTS; a++)
        for (int i = 0; i < BAGS; i++) {
            int64_t hi = next_random();
            lists[a][i] = (hi * 32768 + next_random()) % 100000 + 1;
        }
    int64_t check = 0;
    for (int p = 0; p < 50; p++)
        for (int a = 0; a < LISTS; a++)
            check = (check * 31 + distribute_cookies(lists[a], 2 + (a + p) % 7)) % 1000000007;
    printf("50 passes over 2000 lists of 8 bags: checksum %lld\n", (long long)check);
    return 0;
}
