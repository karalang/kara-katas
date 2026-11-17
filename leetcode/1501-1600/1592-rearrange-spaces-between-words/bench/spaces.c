// LeetCode #1592: Rearrange Spaces Between Words -- the bench in C,
// mirroring spaces.kara: the words found as (start, end) places, the
// spaces counted, the answer written into a new buffer per call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *reorder_spaces(const char *text, int64_t n) {
    int64_t *starts = malloc(n * sizeof(int64_t)), *ends = malloc(n * sizeof(int64_t));
    int64_t words = 0, spaces = 0;
    for (int64_t i = 0; i < n;) {
        if (text[i] == ' ') {
            spaces++;
            i++;
        } else {
            starts[words] = i;
            while (i < n && text[i] != ' ') i++;
            ends[words++] = i;
        }
    }
    int64_t gaps = words - 1;
    int64_t between = gaps == 0 ? 0 : spaces / gaps;
    char *out = malloc(n + 1);
    int64_t len = 0;
    for (int64_t k = 0; k < words; k++) {
        if (k > 0) {
            memset(out + len, ' ', between);
            len += between;
        }
        memcpy(out + len, text + starts[k], ends[k] - starts[k]);
        len += ends[k] - starts[k];
    }
    memset(out + len, ' ', n - len);
    out[n] = 0;
    free(starts);
    free(ends);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1592;
    const int64_t n = 100000;
    char *texts[200];
    for (int t = 0; t < 200; t++) {
        char *b = malloc(n + 1);
        for (int64_t i = 0; i < n; i++) {
            int64_t r = next_random(&seed) % 6;
            b[i] = r < 2 ? ' ' : (char)('a' + (r - 2) % 3);
        }
        int64_t hi = next_random(&seed);
        b[(hi * 32768 + next_random(&seed)) % n] = 'a';
        b[n] = 0;
        texts[t] = b;
    }
    int64_t check = 0, trailing = 0;
    for (int t = 0; t < 200; t++) {
        char *answer = reorder_spaces(texts[t], n);
        for (int64_t i = n - 1; i >= 0 && answer[i] == ' '; i--) trailing++;
        for (int64_t i = 0; i < n; i++) check = (check * 31 + (unsigned char)answer[i] + 1) % 1000000007;
        free(answer);
    }
    printf("200 texts of 100000 characters: %lld trailing spaces, checksum %lld\n", (long long)trailing, (long long)check);
    return 0;
}
