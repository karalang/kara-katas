// Benchmark: LeetCode #949 Largest Time for Given Digits -- the ★ arm,
// every arrangement, on all 10000 arrays of four digits. Mirrors
// largest_time_from_digits.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 10000

static char *largest_time_from_digits(const int64_t *arr) {
    int64_t best = -1;
    for (int64_t i = 0; i < 4; i++) {
        for (int64_t j = 0; j < 4; j++) {
            if (j == i) continue;
            for (int64_t k = 0; k < 4; k++) {
                if (k == i || k == j) continue;
                int64_t l = 6 - i - j - k;
                int64_t hours = arr[i] * 10 + arr[j];
                int64_t minutes = arr[k] * 10 + arr[l];
                if (hours < 24 && minutes < 60 && hours * 60 + minutes > best) best = hours * 60 + minutes;
            }
        }
    }
    char *s = malloc(6);
    if (best < 0) {
        s[0] = '\0';
        return s;
    }
    snprintf(s, 6, "%lld%lld:%lld%lld", (long long)(best / 600), (long long)(best / 60 % 10),
             (long long)(best % 60 / 10), (long long)(best % 10));
    return s;
}

static int64_t arrays[COUNT][4];

int main(void) {
    const int64_t rounds = 500, count = COUNT;
    for (int64_t a = 0; a < count; a++) {
        arrays[a][0] = a / 1000;
        arrays[a][1] = a / 100 % 10;
        arrays[a][2] = a / 10 % 10;
        arrays[a][3] = a % 10;
    }
    int64_t times = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            char *s = largest_time_from_digits(arrays[(r * 37 + i) % count]);
            int64_t v = 0;
            size_t len = strlen(s);
            for (size_t c = 0; c < len; c++) v = v * 131 + (unsigned char)s[c];
            if (len > 0) times++;
            check = (check * 1000003 + v) % 1000000007;
            free(s);
        }
    }
    printf("%lld rounds over all %lld arrays of four digits: %lld times, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)times, (long long)check);
    return 0;
}
