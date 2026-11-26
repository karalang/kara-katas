// LeetCode #1494: Parallel Courses II -- the bench in C, mirroring
// min_number_of_semesters.kara: a DP over the sets of courses taken.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int popcount(int64_t x) {
    int c = 0;
    while (x) {
        x &= x - 1;
        c++;
    }
    return c;
}

static int32_t min_number_of_semesters(int n, const int32_t (*relations)[2], int m, int32_t k) {
    int64_t pre[15] = {0};
    for (int r = 0; r < m; r++) pre[relations[r][1] - 1] |= (int64_t)1 << (relations[r][0] - 1);
    int64_t full = ((int64_t)1 << n) - 1;
    int32_t *semesters = malloc(sizeof(int32_t) * (full + 1));
    for (int64_t i = 0; i <= full; i++) semesters[i] = INT32_MAX;
    semesters[0] = 0;
    for (int64_t taken = 0; taken < full; taken++) {
        if (semesters[taken] == INT32_MAX) continue;
        int64_t open = 0;
        for (int i = 0; i < n; i++)
            if ((taken & ((int64_t)1 << i)) == 0 && (pre[i] & taken) == pre[i]) open |= (int64_t)1 << i;
        int32_t next = semesters[taken] + 1;
        if (popcount(open) <= k) {
            if (next < semesters[taken | open]) semesters[taken | open] = next;
            continue;
        }
        for (int64_t pick = open; pick > 0; pick = (pick - 1) & open)
            if (popcount(pick) == k && next < semesters[taken | pick]) semesters[taken | pick] = next;
    }
    int32_t answer = semesters[full];
    free(semesters);
    return answer;
}

static int64_t seed;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    int32_t relations[105][2];
    for (int64_t call = 0; call < 300; call++) {
        seed = check + call;
        int64_t dense = next_random() % 8;
        int64_t k = 2 + next_random() % 4;
        int m = 0;
        for (int a = 1; a <= 15; a++)
            for (int b = a + 1; b <= 15; b++)
                if (next_random() % 100 < dense) {
                    relations[m][0] = a;
                    relations[m][1] = b;
                    m++;
                }
        check = (check * 31 + min_number_of_semesters(15, (const int32_t (*)[2])relations, m, (int32_t)k)) % 1000000007;
    }
    printf("300 calls on 15 courses: checksum %lld\n", (long long)check);
    return 0;
}
