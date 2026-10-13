// Benchmark for #517: C mirror of the ★ arm (the flow across each gap);
// see find_min_moves.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_min_moves(const int64_t *machines, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += machines[i];
    if (total % n != 0) return -1;
    int64_t average = total / n;
    int64_t moves = 0, surplus = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t extra = machines[i] - average;
        surplus += extra;
        int64_t flow = llabs(surplus);
        if (flow > moves) moves = flow;
        if (extra > moves) moves = extra;
    }
    return moves;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 100 random rows of 10,000 machines (the problem's most) holding up
    // to 100,000 dresses each, every other row topped up so the dresses
    // share out evenly, built once. Then each is solved 300 times.
    int64_t seed = 517, rows = 100;
    int64_t *all = malloc(rows * 10000 * sizeof(int64_t));
    for (int64_t t = 0; t < rows; t++) {
        int64_t *machines = all + t * 10000, total = 0;
        for (int i = 0; i < 10000; i++) {
            int64_t a = next_random(&seed);
            int64_t b = next_random(&seed);
            machines[i] = (a * 32768 + b) % 100001;
            total += machines[i];
        }
        if (t % 2 == 0) machines[9999] += (10000 - total % 10000) % 10000;
    }
    int64_t checksum = 0;
    for (int r = 0; r < 300; r++)
        for (int64_t t = 0; t < rows; t++)
            checksum = (checksum * 31 + find_min_moves(all + t * 10000, 10000) + 1) % 1000000007;
    printf("%lld rows of 10000 machines, 300 times each: checksum %lld\n", (long long)rows,
           (long long)checksum);
    return 0;
}
