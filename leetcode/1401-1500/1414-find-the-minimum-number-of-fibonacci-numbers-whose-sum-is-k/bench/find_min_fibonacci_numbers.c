// LeetCode #1414 bench, C: the Fibonacci numbers up to k, and the largest
// that fits taken each time, workload and checksum as
// find_min_fibonacci_numbers.kara. The list lives in a growable buffer, as
// the Kāra and Rust `Vec` does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t find_min_fibonacci_numbers(int32_t k) {
    size_t cap = 2, len = 2;
    int32_t *fib = malloc(cap * sizeof(int32_t));
    fib[0] = 1;
    fib[1] = 1;
    while (fib[len - 1] <= k - fib[len - 2]) {
        if (len == cap) {
            cap *= 2;
            fib = realloc(fib, cap * sizeof(int32_t));
        }
        fib[len] = fib[len - 1] + fib[len - 2];
        len++;
    }
    int32_t left = k, count = 0;
    for (size_t i = len; i-- > 0;) {
        if (fib[i] <= left) {
            left -= fib[i];
            count++;
        }
    }
    free(fib);
    return count;
}

int main(void) {
    int64_t seed = 1414, check = 0;
    for (int r = 0; r < 3000000; r++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t k = 1 + seed % 1000000000;
        check = (check * 131 + find_min_fibonacci_numbers((int32_t)k)) % 1000000007;
    }
    printf("3 * 10^6 values of k: checksum %lld\n", (long long)check);
    return 0;
}
