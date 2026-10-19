// Benchmark for #780: Reaching Points -- mirror of the ★ arm (backwards
// by remainders), with the same workload as the Kāra program.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

static bool reaching_points(int64_t sx, int64_t sy, int64_t tx, int64_t ty) {
    int64_t x = tx, y = ty;
    while (x > sx && y > sy && x != y) {
        if (x > y) {
            x %= y;
        } else {
            y %= x;
        }
    }
    if (x == sx && y == sy) return true;
    if (x == sx && y > sy) return (y - sy) % x == 0;
    if (y == sy && x > sx) return (x - sx) % y == 0;
    return false;
}

static int64_t seed = 780;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 1024 };
    static int64_t q[COUNT][4];
    for (int64_t i = 0; i < COUNT; i++) {
        int64_t sx = 1 + next_random() % 1000;
        int64_t sy = 1 + next_random() % 1000;
        int64_t a = i % 4 == 3 ? sx + 1 : sx, b = sy;
        while (a <= 500000000 && b <= 500000000) {
            if (next_random() % 2 == 0) {
                a += b;
            } else {
                b += a;
            }
        }
        if (i % 4 == 2) b -= 1;
        q[i][0] = sx; q[i][1] = sy; q[i][2] = a; q[i][3] = b;
    }
    int64_t yes = 0, checksum = 0;
    for (int64_t round = 0; round < 15000; round++) {
        for (int64_t i = 0; i < COUNT; i++) {
            if (reaching_points(q[i][0], q[i][1], q[i][2], q[i][3])) {
                yes++;
                checksum = (checksum * 31 + i + round) % 1000000007;
            }
        }
    }
    printf("15000 rounds of 1024 queries: %lld reachable, checksum %lld\n", (long long)yes, (long long)checksum);
    return 0;
}
