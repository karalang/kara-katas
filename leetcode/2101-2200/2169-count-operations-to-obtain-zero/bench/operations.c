// LeetCode #2169: Count Operations to Obtain Zero -- the benchmark's C
// mirror of operations.kara.

#include <stdint.h>
#include <stdio.h>

static int64_t count_operations(int64_t num1, int64_t num2) {
    int64_t a = num1 > num2 ? num1 : num2;
    int64_t b = num1 > num2 ? num2 : num1;
    int64_t ops = 0;
    while (b > 0) {
        ops += a / b;
        int64_t rest = a % b;
        a = b;
        b = rest;
    }
    return ops;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int64_t a = 0; a <= 3000; a++) {
        for (int64_t b = 0; b <= 3000; b++) {
            int64_t ops = count_operations(a, b);
            total += ops;
            check = (check * 31 + ops) % 1000000007;
        }
    }
    printf("9006001 solves: %lld in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
