#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t max_score(const int32_t *card_points, int64_t n, int32_t k) {
    int32_t sum = 0;
    for (int64_t i = 0; i < k; i++) sum += card_points[i];
    int32_t best = sum;
    for (int64_t i = 0; i < k; i++) {
        sum += card_points[n - 1 - i] - card_points[k - 1 - i];
        if (sum > best) best = sum;
    }
    return best;
}

int main(void) {
    int64_t seed = 1423;
    int32_t *pool = malloc(sizeof(int32_t) * 1000000);
    for (int i = 0; i < 1000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool[i] = (int32_t)(1 + seed / 65536 % 10000);
    }
    int64_t check = 0;
    for (int w = 0; w < 50000; w++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t start = seed / 65536 % 900001;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int32_t k = (int32_t)(1 + seed / 65536 % 100000);
        check = (check * 131 + max_score(pool + start, 100000, k)) % 1000000007;
    }
    printf("5 * 10^4 windows of 10^5 cards: checksum %lld\n", (long long)check);
    free(pool);
    return 0;
}
