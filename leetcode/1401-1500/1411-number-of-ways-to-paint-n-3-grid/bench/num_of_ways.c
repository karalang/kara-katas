// LeetCode #1411 bench, C: rows of two colours and of three, 6 of each in
// the first row, workload and checksum as num_of_ways.kara.
#include <stdint.h>
#include <stdio.h>

static int32_t num_of_ways(int32_t n) {
    const int64_t modulus = 1000000007;
    int64_t two = 6, three = 6;
    for (int32_t i = 1; i < n; i++) {
        int64_t next_two = (3 * two + 2 * three) % modulus;
        int64_t next_three = (2 * two + 2 * three) % modulus;
        two = next_two;
        three = next_three;
    }
    return (int32_t)((two + three) % modulus);
}

int main(void) {
    int64_t check = 0;
    for (int64_t k = 0; k < 40000; k++) {
        int64_t n = 1 + (check + k) % 5000;
        check = (check * 131 + num_of_ways((int32_t)n)) % 1000000007;
    }
    printf("40000 grids of up to 5000 rows: checksum %lld\n", (long long)check);
    return 0;
}
