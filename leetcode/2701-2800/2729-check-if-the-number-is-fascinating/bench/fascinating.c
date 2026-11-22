// LeetCode #2729: Check if The Number is Fascinating -- the bench
// (fascinating.kara in C): n, 2 n and 3 n joined by `snprintf`, the
// digits sorted by insertion and compared with "123456789".
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int is_fascinating(int64_t n) {
    char joined[64];
    int len = snprintf(joined, sizeof joined, "%lld%lld%lld", (long long)n, (long long)(2 * n), (long long)(3 * n));
    for (int i = 1; i < len; i++) {
        char c = joined[i];
        int j = i - 1;
        while (j >= 0 && joined[j] > c) {
            joined[j + 1] = joined[j];
            j--;
        }
        joined[j + 1] = c;
    }
    return strcmp(joined, "123456789") == 0;
}

static int64_t seed = 2729;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 1000000, rounds = 5;
    const int64_t fascinating[4] = {192, 219, 273, 327};
    int64_t *numbers = malloc(sizeof(int64_t) * count);
    for (int i = 0; i < count; i++) numbers[i] = i % 50 == 0 ? fascinating[next_random() % 4] : next_random() % 900 + 100;
    int64_t yes = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < count; i++) {
            int answer = is_fascinating(numbers[i]);
            if (answer) yes++;
            check = (check * 31 + (answer ? 2 : 1) + r) % 1000000007;
        }
    }
    printf("%d numbers, %d rounds: %lld fascinating, checksum %lld\n", count, rounds, (long long)yes, (long long)check);
    free(numbers);
    return 0;
}
