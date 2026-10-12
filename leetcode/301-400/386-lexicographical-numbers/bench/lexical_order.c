// Benchmark for #386: mirror of lexical_order.kara (step to the next number).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *lexical_order(int64_t n) {
    int64_t *out = malloc(n * sizeof(int64_t));
    int64_t cur = 1;
    for (int64_t i = 0; i < n; i++) {
        out[i] = cur;
        if (cur * 10 <= n) {
            cur *= 10;
        } else {
            while (cur % 10 == 9 || cur + 1 > n) cur /= 10;
            cur += 1;
        }
    }
    return out;
}

int main(void) {
    int64_t checksum = 0;
    for (int64_t q = 0; q < 6000; q++) {
        int64_t n = 50000 - q % 1000;
        int64_t *v = lexical_order(n);
        int64_t sum = 0;
        for (int64_t k = 0; k < n; k++) sum += v[k] * (k + 1);
        checksum = (checksum * 31 + sum) % 1000000007;
        free(v);
    }
    printf("6000 lists, checksum %lld\n", (long long)checksum);
    return 0;
}
