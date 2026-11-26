// LeetCode #1402 bench, C: the same sort and running sum, workload and
// checksum as max_satisfaction.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define POOL 100000
#define WINDOW 500

static int by_value(const void *pa, const void *pb) {
    int32_t a = *(const int32_t *)pa, b = *(const int32_t *)pb;
    return (a > b) - (a < b);
}

static int32_t max_satisfaction(const int32_t *satisfaction, int n) {
    int32_t order[WINDOW];
    memcpy(order, satisfaction, sizeof(int32_t) * n);
    qsort(order, n, sizeof(int32_t), by_value);
    int32_t running = 0, total = 0;
    for (int i = n - 1; i >= 0; i--) {
        if (running + order[i] <= 0) {
            break;
        }
        running += order[i];
        total += running;
    }
    return total;
}

int main(void) {
    static int32_t pool[POOL];
    int64_t seed = 1402;
    for (int i = 0; i < POOL; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        pool[i] = (int32_t)(seed % 2001 - 1000);
    }
    int64_t check = 0;
    int32_t window[WINDOW];
    for (int64_t r = 0; r < 20000; r++) {
        int64_t at = (check + r * 7919) % 99501;
        memcpy(window, pool + at, sizeof(int32_t) * WINDOW);
        check = (check * 131 + max_satisfaction(window, WINDOW)) % 1000000007;
    }
    printf("20000 windows of 500 dishes: checksum %lld\n", (long long)check);
    return 0;
}
