// LeetCode #1416 bench, C: ways[i] counts the arrays the digits from i on
// can be read as, workload and checksum as number_of_arrays.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t number_of_arrays(const char *s, size_t n, int32_t k) {
    const int64_t modulus = 1000000007;
    int64_t *ways = calloc(n + 1, sizeof(int64_t));
    ways[n] = 1;
    for (size_t i = n; i-- > 0;) {
        if (s[i] == '0') {
            continue;
        }
        int64_t number = 0;
        for (size_t j = i; j < n; j++) {
            number = number * 10 + (s[j] - '0');
            if (number > k) {
                break;
            }
            ways[i] = (ways[i] + ways[j + 1]) % modulus;
        }
    }
    int32_t answer = (int32_t)ways[0];
    free(ways);
    return answer;
}

int main(void) {
    int64_t seed = 1416, check = 0;
    char *pool = malloc(200000);
    int last_zero = 1;
    for (int i = 0; i < 200000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t r = seed / 65536;
        int zero = !last_zero && r % 10 == 0;
        pool[i] = zero ? '0' : (char)('1' + r % 9);
        last_zero = zero;
    }
    for (int w = 0; w < 100; w++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        size_t start = (size_t)(seed / 65536 % 100000);
        while (pool[start] == '0') {
            start++;
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t k = 1 + seed % 1000000000;
        check = (check * 131 + number_of_arrays(pool + start, 100000, (int32_t)k)) % 1000000007;
    }
    printf("100 windows of 10^5 digits: checksum %lld\n", (long long)check);
    free(pool);
    return 0;
}
