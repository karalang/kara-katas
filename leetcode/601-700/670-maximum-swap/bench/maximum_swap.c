// Benchmark for #670: the last place of each digit, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>

static int64_t maximum_swap(int64_t num) {
    int64_t d[20];
    int64_t n = 0;
    int64_t x = num;
    while (x > 0) {
        d[n++] = x % 10;
        x /= 10;
    }
    if (n == 0) {
        d[n++] = 0;
    }
    for (int64_t i = 0, j = n - 1; i < j; i++, j--) {
        int64_t t = d[i];
        d[i] = d[j];
        d[j] = t;
    }
    int64_t last[10];
    for (int v = 0; v < 10; v++) {
        last[v] = -1;
    }
    for (int64_t i = 0; i < n; i++) {
        last[d[i]] = i;
    }
    for (int64_t i = 0; i < n; i++) {
        for (int64_t v = 9; v > d[i]; v--) {
            if (last[v] > i) {
                int64_t j = last[v];
                d[j] = d[i];
                d[i] = v;
                int64_t r = 0;
                for (int64_t k = 0; k < n; k++) {
                    r = r * 10 + d[k];
                }
                return r;
            }
        }
    }
    return num;
}

int main(void) {
    int64_t count = 3000000;
    int64_t sum = 0;
    for (int64_t i = 0; i < count; i++) {
        sum = (sum * 31 + maximum_swap(i * 33 + i % 7)) % 1000000007;
    }
    printf("%lld numbers: checksum %lld\n", (long long)count, (long long)sum);
    return 0;
}
