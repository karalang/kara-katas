/* Benchmark mirror of LeetCode #318 — build-once + punch.
   Same algorithm as bench/max_product.kara: a flat WORDS x LMAX letter grid,
   26-bit letter masks rebuilt every pass, and a full pair scan that records
   each word's best disjoint partner. One word is rewritten per pass. */
#include <stdio.h>

#define WORDS   6000
#define LMAX    16
#define WINDOW  7
#define PASSES  15
#define MASKMOD 1073741823LL

static long long letters[WORDS * LMAX];
static long long lens[WORDS];
static long long masks[WORDS];
static long long best[WORDS];

static long long next_rand(long long *seed) {
    *seed = (*seed * 1103515245LL + 12345LL) % 2147483648LL;
    return *seed / 65536;
}

static void write_word(long long w, long long *seed) {
    long long len = next_rand(seed) % LMAX + 1;
    long long base = next_rand(seed) % (26 - WINDOW + 1);
    lens[w] = len;
    for (long long k = 0; k < len; k++)
        letters[w * LMAX + k] = base + next_rand(seed) % WINDOW;
}

static void build_masks(void) {
    for (long long w = 0; w < WORDS; w++) {
        long long m = 0;
        for (long long k = 0; k < lens[w]; k++)
            m |= 1LL << letters[w * LMAX + k];
        masks[w] = m;
    }
}

int main(void) {
    long long seed = 318318;
    for (long long w = 0; w < WORDS; w++) write_word(w, &seed);

    long long sink = 0;
    for (long long p = 0; p < PASSES; p++) {
        write_word(p * 977 % WORDS, &seed);
        build_masks();

        for (long long i = 0; i < WORDS; i++) best[i] = 0;
        for (long long i = 0; i < WORDS; i++) {
            long long mi = masks[i], li = lens[i];
            for (long long j = i + 1; j < WORDS; j++) {
                if ((mi & masks[j]) == 0) {
                    long long q = li * lens[j];
                    if (q > best[i]) best[i] = q;
                    if (q > best[j]) best[j] = q;
                }
            }
        }

        long long total = 0, top = 0;
        for (long long i = 0; i < WORDS; i++) {
            total += best[i];
            if (best[i] > top) top = best[i];
        }
#ifdef DEBUG_PASSES
        printf("pass %lld total %lld top %lld\n", p, total, top);
#endif
        sink = (sink * 31 + total + top) % MASKMOD;
    }

    printf("checksum %lld\n", sink);
    return 0;
}
