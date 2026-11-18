// LeetCode #2320: Count Number of Ways to Place Houses -- the bench, the
// ★ arm in C. One side's placements ending in an empty plot and in a
// house rolled forward a plot at a time, and their sum squared. O(n).

#include <stdint.h>
#include <stdio.h>

static int64_t count_house_placements(int64_t n) {
    const int64_t modulus = 1000000007;
    int64_t empty = 1, house = 1;
    for (int64_t i = 1; i < n; i++) {
        int64_t next_empty = (empty + house) % modulus;
        house = empty;
        empty = next_empty;
    }
    int64_t side = (empty + house) % modulus;
    return side * side % modulus;
}

int main(void) {
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++)
        for (int64_t n = 1; n <= 10000; n++)
            check = (check * 31 + count_house_placements(n) + p) % 1000000007;
    printf("10 passes over every count of plots up to 10^4: checksum %lld\n", (long long)check);
    return 0;
}
