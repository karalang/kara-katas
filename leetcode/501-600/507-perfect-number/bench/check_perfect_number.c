// Benchmark for #507 in C: the ★ arm (divisors in pairs up to the square
// root); see ../check_perfect_number.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool check_perfect_number(int64_t num) {
    if (num == 1) return false;
    int64_t sum = 1;
    for (int64_t i = 2; i * i <= num; i++) {
        if (num % i == 0) {
            sum += i;
            if (i * i != num) sum += num / i;
        }
    }
    return sum == num;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 100,000 numbers from 1 to 10^8 (the problem's most), one in ten of
    // them one of the five perfect numbers in range, built once. Then
    // each is checked once.
    const int64_t count = 100000;
    static const int64_t known[5] = {6, 28, 496, 8128, 33550336};
    int64_t seed = 507;
    int64_t *nums = malloc((size_t)count * sizeof(int64_t));
    for (int64_t c = 0; c < count; c++) {
        if (c % 10 == 0) {
            nums[c] = known[next_random(&seed) % 5];
        } else {
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            nums[c] = 1 + (hi * 32768 + lo) % 100000000;
        }
    }
    int64_t perfect = 0, checksum = 0;
    for (int64_t c = 0; c < count; c++) {
        bool answer = check_perfect_number(nums[c]);
        if (answer) perfect++;
        checksum = (checksum * 31 + nums[c] % 1000 * 2 + (answer ? 1 : 0)) % 1000000007;
    }
    printf("%lld numbers: %lld perfect, checksum %lld\n", (long long)count, (long long)perfect,
           (long long)checksum);
    free(nums);
    return 0;
}
