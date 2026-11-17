// LeetCode #2248: Intersection of Multiple Arrays -- the benchmark's C
// mirror of common.kara: a count for every value from 1 to 1000, kept
// where it reaches the number of arrays.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t nums[10][100], count[1001], common[1001];

static int64_t intersection(int rows, int cols) {
    memset(count, 0, sizeof count);
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) count[nums[r][c]]++;
    int64_t len = 0;
    for (int64_t v = 1; v <= 1000; v++)
        if (count[v] == rows) common[len++] = v;
    return len;
}

static int64_t seed = 2248;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0, pool[150];
    for (int i = 0; i < 150; i++) pool[i] = i + 1;
    for (int t = 0; t < 20000; t++) {
        for (int r = 0; r < 10; r++) {
            for (int i = 0; i < 100; i++) {
                int j = i + (int)(next_random() % (150 - i));
                int64_t x = pool[i];
                pool[i] = pool[j];
                pool[j] = x;
            }
            memcpy(nums[r], pool, sizeof nums[r]);
        }
        int64_t len = intersection(10, 100), acc = len;
        for (int64_t i = 0; i < len; i++) acc = (acc * 1009 + common[i]) % 1000000007;
        check = (check * 31 + acc) % 1000000007;
    }
    printf("20000 cases: checksum %lld\n", (long long)check);
    return 0;
}
