// LeetCode #1779: Find Nearest Point That Has the Same X or Y Coordinate --
// the bench in C, mirroring nearest_valid_point.kara: one pass keeping the
// nearest valid point so far.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int nearest_valid_point(int x, int y, const int (*points)[2], long n) {
    int best = -1;
    int nearest = INT32_MAX;
    for (long i = 0; i < n; i++) {
        int a = points[i][0], b = points[i][1];
        if (a == x || b == y) {
            int d = abs(a - x) + abs(b - y);
            if (d < nearest) {
                nearest = d;
                best = (int)i;
            }
        }
    }
    return best;
}

static int64_t seed = 1779;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int (*lists[20])[2];
    for (int l = 0; l < 20; l++) {
        lists[l] = malloc(sizeof(int[2]) * 10000);
        for (int k = 0; k < 10000; k++) {
            int64_t a = 1 + next_random() % 100;
            int64_t b = 1 + next_random() % 100;
            lists[l][k][0] = (int)a;
            lists[l][k][1] = (int)b;
        }
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 20000; call++) {
        int64_t x = 1 + (check + call) % 100;
        int64_t y = 1 + (check / 100 + call * 7) % 100;
        int found = nearest_valid_point((int)x, (int)y, (const int (*)[2])lists[call % 20], 10000);
        check = (check * 31 + found + 1) % 1000000007;
    }
    printf("20000 calls over 20 lists: checksum %lld\n", (long long)check);
    for (int l = 0; l < 20; l++) free(lists[l]);
    return 0;
}
