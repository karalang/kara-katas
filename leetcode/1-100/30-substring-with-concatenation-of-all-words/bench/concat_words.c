/* Benchmark workload — substring-with-concatenation, LeetCode #30 (sliding window).
 *
 * Algorithmic mirror of concat_words.kara, compiled with `clang -O3`. Same
 * 16-word vocabulary, same glibc LCG (high bits for the vocab pick), same
 * NSLOTS / RUNS, same O(n) sliding-window search, same sink.
 *
 * Words are length 4 over ASCII, so each one packs into a 32-bit key and the
 * count tables become tiny id-indexed arrays (the natural C shape, no string
 * hashing). `need`/`seen` only ever hold the <= K distinct target words, so a
 * linear id lookup over them is the moral equivalent of the map probe the
 * other mirrors do. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static inline unsigned pack(const char *p) {
    return (unsigned)(unsigned char)p[0] | ((unsigned)(unsigned char)p[1] << 8) |
           ((unsigned)(unsigned char)p[2] << 16) | ((unsigned)(unsigned char)p[3] << 24);
}

static inline int need_id(const unsigned *key, int nd, unsigned k) {
    for (int i = 0; i < nd; i++)
        if (key[i] == k)
            return i;
    return -1;
}

typedef struct {
    long long cnt;
    long long sum_idx;
} Res;

static Res find_substring(const char *s, long long n, const unsigned *word_keys, int k) {
    Res res = {0, 0};
    if (k == 0)
        return res;
    const int wl = 4;
    long long total = (long long)wl * k;
    if (total > n)
        return res;

    unsigned need_key[64];
    long long need_req[64];
    int nd = 0;
    for (int i = 0; i < k; i++) {
        int id = need_id(need_key, nd, word_keys[i]);
        if (id >= 0) {
            need_req[id]++;
        } else {
            need_key[nd] = word_keys[i];
            need_req[nd] = 1;
            nd++;
        }
    }

    long long seen[64];
    for (int r = 0; r < wl; r++) {
        for (int z = 0; z < nd; z++)
            seen[z] = 0;
        long long count = 0, left = r, j = r;
        while (j + wl <= n) {
            int id = need_id(need_key, nd, pack(s + j));
            if (id < 0) {
                for (int z = 0; z < nd; z++)
                    seen[z] = 0;
                count = 0;
                left = j + wl;
            } else {
                seen[id]++;
                count++;
                while (seen[id] > need_req[id]) {
                    int lid = need_id(need_key, nd, pack(s + left));
                    seen[lid]--;
                    left += wl;
                    count--;
                }
                if (count == k) {
                    res.cnt++;
                    res.sum_idx += left;
                    int lid = need_id(need_key, nd, pack(s + left));
                    seen[lid]--;
                    left += wl;
                    count--;
                }
            }
            j += wl;
        }
    }
    return res;
}

int main(void) {
    const long long nslots = 50000;
    const long long runs = 40;

    const char *chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/";
    unsigned vocab_key[16];
    for (int v = 0; v < 16; v++)
        vocab_key[v] = pack(chars + v * 4);

    long long n = nslots * 4;
    char *s = (char *)malloc((size_t)n + 1);
    long long state = 1;
    for (long long t = 0; t < nslots; t++) {
        state = (state * 1103515245LL + 12345) % 2147483648LL;
        long long v = (state / 131072) % 16;
        memcpy(s + t * 4, chars + v * 4, 4);
    }

    long long sink = 0;
    for (long long run = 0; run < runs; run++) {
        long long start = run % 13;
        unsigned word_keys[4];
        for (int d = 0; d < 4; d++)
            word_keys[d] = vocab_key[start + d];
        Res res = find_substring(s, n, word_keys, 4);
        sink += res.cnt;
        sink += res.sum_idx;
    }

    printf("%lld\n", sink);
    free(s);
    return 0;
}
