// Benchmark for #842: Split Array into Fibonacci Sequence -- C twin of the
// Kāra ★ arm (the first two numbers decide the rest).
#include <stdio.h>
#include <string.h>
#include <stdint.h>

static int64_t read_num(const char *d, int64_t start, int64_t len) {
    if (len > 1 && d[start] == '0') return -1;
    int64_t value = 0;
    for (int64_t k = start; k < start + len; k++) value = value * 10 + (d[k] - '0');
    return value > 2147483647 ? -1 : value;
}

// Writes the split into seq and returns its length, or 0 for none.
static int64_t split_into_fibonacci(const char *d, int64_t *seq) {
    int64_t n = (int64_t)strlen(d);
    for (int64_t i = 1; i < 11; i++) {
        for (int64_t j = 1; j < 11; j++) {
            if (i + j >= n) break;
            int64_t a = read_num(d, 0, i), b = read_num(d, i, j);
            if (a < 0 || b < 0) continue;
            int64_t len = 2;
            seq[0] = a;
            seq[1] = b;
            int64_t pos = i + j;
            while (pos < n) {
                int64_t c = seq[len - 1] + seq[len - 2];
                if (c > 2147483647) break;
                char digits[24];
                int64_t w = snprintf(digits, sizeof digits, "%lld", (long long)c);
                if (pos + w > n) break;
                if (memcmp(d + pos, digits, (size_t)w) != 0) break;
                seq[len++] = c;
                pos += w;
            }
            if (pos == n) return len;
        }
    }
    return 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 240000;
    int64_t seed = 842;
    static char cases[64][256];
    const int64_t tops[3] = {10, 1000, 100000};
    for (int64_t g = 0; g < count; g++) {
        int64_t top = tops[g % 3];
        int64_t x = next_random(&seed) % top;
        int64_t y = next_random(&seed) % top;
        char *s = cases[g];
        int64_t len = snprintf(s, 256, "%lld%lld", (long long)x, (long long)y);
        for (;;) {
            int64_t z = x + y;
            char w[24];
            int64_t wl = snprintf(w, sizeof w, "%lld", (long long)z);
            if (z > 2147483647 || len + wl > 200) break;
            memcpy(s + len, w, (size_t)wl + 1);
            len += wl;
            x = y;
            y = z;
        }
        if (g % 4 == 3) {
            int64_t at = next_random(&seed) % len;
            s[at] = (char)('0' + (s[at] - '0' + 1) % 10);
        }
    }
    int64_t seq[256];
    int64_t split = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t len = split_into_fibonacci(cases[round % count], seq);
        if (len > 0) {
            split++;
            checksum = (checksum * 31 + len * 1000 + seq[len - 1] % 1000) % 1000000007;
        } else {
            checksum = (checksum * 31 + 7) % 1000000007;
        }
    }
    printf("%lld rounds of %lld strings: %lld split, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)split, (long long)checksum);
    return 0;
}
