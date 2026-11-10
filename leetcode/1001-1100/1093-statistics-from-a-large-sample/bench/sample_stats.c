// Benchmark: LeetCode #1093 Statistics from a Large Sample -- the ★ arm, two
// walks over the counts. Mirrors sample_stats.kara.
#include <stdint.h>
#include <stdio.h>

static void sample_stats(const int64_t *count, int n, double out[5]) {
    int64_t low = -1, high = 0, sum = 0, total = 0, mode = 0;
    for (int64_t k = 0; k < n; k++) {
        int64_t c = count[k];
        if (c == 0) continue;
        if (low < 0) low = k;
        high = k;
        sum += k * c;
        total += c;
        if (c > count[mode]) mode = k;
    }
    int64_t left = (total - 1) / 2, right = total / 2;
    int64_t seen = 0, median_low = -1, median_high = -1;
    for (int64_t k = 0; k < n; k++) {
        seen += count[k];
        if (median_low < 0 && seen > left) median_low = k;
        if (seen > right) {
            median_high = k;
            break;
        }
    }
    out[0] = (double)low;
    out[1] = (double)high;
    out[2] = (double)sum / (double)total;
    out[3] = (double)(median_low + median_high) / 2.0;
    out[4] = (double)mode;
}

static int64_t seed = 1093;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t samples[64][256];
    for (int k = 0; k < 64; k++) {
        for (int i = 0; i < 4 + k * 4; i++) {
            int64_t p = next_random() % 256;
            samples[k][p] = next_random() * 91 % 3000000 + 1;
        }
    }
    int64_t modes = 0, check = 0;
    double s[5];
    for (int64_t round = 0; round < 10000; round++) {
        for (int64_t j = 0; j < 64; j++) {
            samples[j][(round * 7 + j * 13) % 256] += 1;
            sample_stats(samples[j], 256, s);
            modes += (int64_t)s[4];
            for (int i = 0; i < 5; i++) check = (check * 31 + (int64_t)(s[i] * 1000000.0)) % 1000000007;
        }
    }
    printf("10000 rounds over 64 samples: modes sum to %lld, checksum %lld\n", (long long)modes, (long long)check);
    return 0;
}
