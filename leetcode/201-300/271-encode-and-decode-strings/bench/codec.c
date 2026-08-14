/* Benchmark workload for LeetCode #271 — Encode and Decode Strings.
 *
 * Algorithm-for-algorithm mirror of codec.kara. See that file's header for
 * what this lane measures and for the two parity decisions (hand-rolled
 * decimal in every language; every buffer hoisted out of the punch loop). */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const int64_t count = 50000;
    const int64_t rounds = 250;

    /* ---- build once: a flat corpus ---------------------------------- */
    int64_t cap_src = count * 25;
    unsigned char *src = malloc((size_t)cap_src);
    int64_t *off = malloc((size_t)count * sizeof(int64_t));
    int64_t *len = malloc((size_t)count * sizeof(int64_t));
    int64_t src_len = 0;
    int64_t state = 271271;
    for (int64_t i = 0; i < count; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        int64_t n = (state / 65536) % 25;
        off[i] = src_len;
        len[i] = n;
        for (int64_t p = 0; p < n; p++) {
            state = (state * 1103515245 + 12345) & 2147483647;
            src[src_len++] = (unsigned char)(97 + (state / 65536) % 26);
        }
    }

    /* ---- hoisted working buffers ------------------------------------ */
    int64_t enc_cap = src_len + count * 3;
    unsigned char *enc = calloc((size_t)enc_cap, 1);
    unsigned char *dout = calloc((size_t)src_len, 1);

    /* ---- punch ------------------------------------------------------ */
    int64_t sink = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t w = 0;
        for (int64_t k = 0; k < count; k++) {
            int64_t n = len[k];
            if (n >= 10) {
                enc[w++] = (unsigned char)(48 + n / 10);
            }
            enc[w++] = (unsigned char)(48 + n % 10);
            enc[w++] = 35; /* '#' */
            int64_t base = off[k];
            for (int64_t p = 0; p < n; p++) {
                enc[w + p] = src[base + p];
            }
            w += n;
        }
        int64_t encoded_len = w;

        int64_t rp = 0, dp = 0, items = 0, check = 0;
        while (rp < encoded_len) {
            int64_t n = 0;
            while (enc[rp] != 35) {
                n = n * 10 + ((int64_t)enc[rp] - 48);
                rp++;
            }
            rp++;
            for (int64_t p = 0; p < n; p++) {
                dout[dp + p] = enc[rp + p];
            }
            check = (check * 31 + n) % 1000000007;
            rp += n;
            dp += n;
            items++;
        }
        sink = (sink * 131 + check + items) % 1000000007;
    }

    printf("%lld\n", (long long)sink);
    free(src); free(off); free(len); free(enc); free(dout);
    return 0;
}
