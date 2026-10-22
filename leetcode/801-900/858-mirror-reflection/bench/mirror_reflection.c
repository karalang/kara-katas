// Benchmark for #858: Mirror Reflection -- C twin of the Kāra trace arm (the
// ray traced from wall to wall), in every room LeetCode allows.
#include <stdint.h>
#include <stdio.h>

static int64_t mirror_reflection(int64_t p, int64_t q) {
    int64_t y = 0;
    int up = 1, east = 0;
    for (;;) {
        if (up) {
            y += q;
            if (y > p) {
                y = 2 * p - y;
                up = 0;
            }
        } else {
            y -= q;
            if (y < 0) {
                y = -y;
                up = 1;
            }
        }
        east = !east;
        if (y == p) return east ? 1 : 2;
        // the south-west corner is never reached, so this is the east wall
        if (y == 0) return 0;
    }
}

int main(void) {
    int64_t counts[3] = {0, 0, 0};
    int64_t check = 0;
    for (int64_t p = 1; p <= 1000; p++) {
        for (int64_t q = 1; q <= p; q++) {
            int64_t r = mirror_reflection(p, q);
            counts[r]++;
            check = (check * 3 + r) % 1000000007;
        }
    }
    printf("500500 rooms: receptor 0 %lld times, 1 %lld, 2 %lld, checksum %lld\n", (long long)counts[0],
           (long long)counts[1], (long long)counts[2], (long long)check);
    return 0;
}
