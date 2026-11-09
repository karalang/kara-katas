// LeetCode #2048 -- the ★ arm as a benchmark; mirror of beautiful.kara.
#include <stdint.h>
#include <stdio.h>

static int is_balanced(int64_t x) {
    int64_t counts[10] = {0};
    int64_t y = x;
    while (y > 0) {
        counts[y % 10]++;
        y /= 10;
    }
    for (int64_t d = 0; d < 10; d++) {
        if (counts[d] != 0 && counts[d] != d) return 0;
    }
    return 1;
}

static int64_t next_beautiful_number(int64_t n) {
    int64_t x = n + 1;
    while (!is_balanced(x)) x++;
    return x;
}

int main(void) {
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t k = 0; k < 1000; k++) {
        int64_t x = next_beautiful_number(k * 1000 + k * 7 % 1000);
        calls++;
        sum += x;
        check = (check * 31 + x) % 1000000007;
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum,
           (long long)check);
    return 0;
}
