#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* The answers into a fresh array, as the Kara arm collects a Vec[bool]. */
static bool *kids_with_candies(const int32_t *candies, int64_t n, int32_t extra_candies) {
    int32_t most = candies[0];
    for (int64_t i = 1; i < n; i++)
        if (candies[i] > most) most = candies[i];
    bool *answer = malloc(n);
    for (int64_t i = 0; i < n; i++) answer[i] = candies[i] + extra_candies >= most;
    return answer;
}

int main(void) {
    int64_t seed = 1431;
    int32_t *pool = malloc(sizeof(int32_t) * 1000000);
    for (int i = 0; i < 1000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool[i] = (int32_t)(1 + seed / 65536 % 100);
    }
    int64_t check = 0;
    for (int w = 0; w < 1000000; w++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t start = seed / 65536 % 999901;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int32_t extra = (int32_t)(1 + seed / 65536 % 50);
        bool *answer = kids_with_candies(pool + start, 100, extra);
        int64_t bits = 0;
        for (int i = 0; i < 100; i++)
            if (answer[i]) bits += i + 1;
        free(answer);
        check = (check * 131 + bits) % 1000000007;
    }
    printf("10^6 windows of 100 kids: checksum %lld\n", (long long)check);
    free(pool);
    return 0;
}
