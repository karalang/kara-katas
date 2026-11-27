// LeetCode #1798: Maximum Number of Consecutive Values You Can Make -- the
// bench in C: the ★ arm over 200 random lists of 2000 coins built once,
// 20000 calls. The copy is sorted with qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_value(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static int32_t get_maximum_consecutive(const int32_t *coins, int n) {
    int32_t *sorted = malloc(n * sizeof(int32_t));
    memcpy(sorted, coins, n * sizeof(int32_t));
    qsort(sorted, n, sizeof(int32_t), by_value);
    int32_t reach = 0;
    for (int i = 0; i < n; i++) {
        if (sorted[i] > reach + 1) break;
        reach += sorted[i];
    }
    free(sorted);
    return reach + 1;
}

static int64_t seed = 1798;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t lists[200][2000];
    for (int l = 0; l < 200; l++)
        for (int x = 0; x < 2000; x++) lists[l][x] = (int32_t)(1 + next_random() % 200);
    int64_t check = 0;
    for (int64_t call = 0; call < 20000; call++) {
        check = (check * 31 + get_maximum_consecutive(lists[(check + call) % 200], 2000)) % 1000000007;
    }
    printf("20000 calls over 200 lists of 2000 coins: checksum %lld\n", (long long)check);
    return 0;
}
