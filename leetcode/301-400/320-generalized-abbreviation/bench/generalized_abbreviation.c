/* Benchmark mirror of LeetCode #320 — same mask walk as
 * bench/generalized_abbreviation.kara. */
#include <stdio.h>
#include <stdint.h>

#define WORD_LEN 20
#define PASSES   8
#define MODULUS  1073741789LL

int main(void) {
    long long sink = 0;
    long long total_chars = 0;

    for (long long p = 0; p < PASSES; p++) {
        unsigned char bs[WORD_LEN];
        for (long long i = 0; i < WORD_LEN; i++)
            bs[i] = (unsigned char)((i * 7 + p * 11) % 26) + 'a';

        unsigned char buf[WORD_LEN + 8];
        long long limit = 1LL << WORD_LEN;
        long long acc = 0;
        long long chars = 0;

        for (long long mask = 0; mask < limit; mask++) {
            long long len = 0;
            long long run = 0;
            for (long long i = 0; i < WORD_LEN; i++) {
                if (mask & (1LL << i)) {
                    run++;
                } else {
                    if (run > 0) {
                        if (run >= 10) buf[len++] = (unsigned char)(run / 10) + '0';
                        buf[len++] = (unsigned char)(run % 10) + '0';
                        run = 0;
                    }
                    buf[len++] = bs[i];
                }
            }
            if (run > 0) {
                if (run >= 10) buf[len++] = (unsigned char)(run / 10) + '0';
                buf[len++] = (unsigned char)(run % 10) + '0';
            }

            for (long long j = 0; j < len; j++)
                acc = (acc * 131 + (long long)buf[j]) % MODULUS;
            acc = (acc * 131 + 7) % MODULUS;
            chars += len;
        }

        sink = (sink * 1000003 + acc) % MODULUS;
        total_chars += chars;
    }

    printf("sink %lld chars %lld\n", sink, total_chars);
    return 0;
}
