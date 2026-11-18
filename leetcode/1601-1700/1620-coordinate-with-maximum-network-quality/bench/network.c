// LeetCode #1620: Coordinate With Maximum Network Quality -- the bench in C,
// mirroring network.kara: every point, every tower, f64 distances.
#include <math.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    int32_t x, y, q;
} Tower;

static void best_coordinate(const Tower *towers, int n, int32_t radius, int32_t out[2]) {
    out[0] = 0;
    out[1] = 0;
    int32_t most = 0;
    for (int32_t x = 0; x <= 50; x++) {
        for (int32_t y = 0; y <= 50; y++) {
            int32_t quality = 0;
            for (int i = 0; i < n; i++) {
                int32_t dx = towers[i].x - x, dy = towers[i].y - y;
                double d = sqrt((double)(dx * dx + dy * dy));
                if (d <= (double)radius) quality += (int32_t)floor((double)towers[i].q / (1.0 + d));
            }
            if (quality > most) {
                most = quality;
                out[0] = x;
                out[1] = y;
            }
        }
    }
}

static int64_t seed = 1620;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static Tower cases[1000][50];
    static int32_t radii[1000];
    for (int c = 0; c < 1000; c++) {
        for (int i = 0; i < 50; i++) {
            cases[c][i].x = (int32_t)(next_random() % 51);
            cases[c][i].y = (int32_t)(next_random() % 51);
            cases[c][i].q = (int32_t)(next_random() % 51);
        }
        radii[c] = (int32_t)(next_random() % 50 + 1);
    }
    int64_t check = 0, spread = 0;
    for (int c = 0; c < 1000; c++) {
        int32_t best[2];
        best_coordinate(cases[c], 50, radii[c], best);
        spread += best[0] + best[1];
        check = (check * 31 + best[0] * 51 + best[1] + 1) % 1000000007;
    }
    printf("1000 cases of 50 towers: coordinates sum to %lld, checksum %lld\n", (long long)spread, (long long)check);
    return 0;
}
