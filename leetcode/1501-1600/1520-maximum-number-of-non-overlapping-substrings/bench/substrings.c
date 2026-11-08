// LeetCode #1520: Maximum Number of Non-Overlapping Substrings -- the
// bench in C: the ★ arm over 200000 random strings of 1 to 64 letters
// over 5, built once and answered 3 times. Each answer copies the string's
// bytes and returns its substrings as fresh allocations, as the other
// languages do.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **items;
    int64_t len;
} Pieces;

static Pieces max_num_of_substrings(const char *s, int64_t n) {
    char *bytes = malloc(n);
    memcpy(bytes, s, n);
    int64_t *first = malloc(26 * sizeof(int64_t));
    int64_t *last = malloc(26 * sizeof(int64_t));
    for (int c = 0; c < 26; c++) {
        first[c] = n;
        last[c] = -1;
    }
    for (int64_t i = 0; i < n; i++) {
        int c = bytes[i] - 97;
        if (i < first[c]) first[c] = i;
        last[c] = i;
    }
    int64_t *lo = malloc(26 * sizeof(int64_t));
    int64_t *hi = malloc(26 * sizeof(int64_t));
    int64_t count = 0, right = -1;
    for (int64_t i = 0; i < n; i++) {
        int c = bytes[i] - 97;
        if (i != first[c]) continue;
        int64_t end = last[c];
        int ok = 1;
        for (int64_t j = i; j <= end; j++) {
            int d = bytes[j] - 97;
            if (first[d] < i) {
                ok = 0;
                break;
            }
            if (last[d] > end) end = last[d];
        }
        if (!ok) continue;
        if (i > right) {
            lo[count] = i;
            hi[count] = end;
            count++;
        } else {
            lo[count - 1] = i;
            hi[count - 1] = end;
        }
        right = end;
    }
    Pieces out;
    out.items = malloc(count * sizeof(char *));
    out.len = count;
    for (int64_t k = 0; k < count; k++) {
        int64_t len = hi[k] - lo[k] + 1;
        char *p = malloc(len + 1);
        memcpy(p, s + lo[k], len);
        p[len] = 0;
        out.items[k] = p;
    }
    free(bytes);
    free(first);
    free(last);
    free(lo);
    free(hi);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const int64_t count = 200000;
    int64_t seed = 1520;
    char **strings = malloc(count * sizeof(char *));
    int64_t *lens = malloc(count * sizeof(int64_t));
    for (int64_t k = 0; k < count; k++) {
        int64_t n = next_random(&seed) % 64 + 1;
        char *s = malloc(n + 1);
        for (int64_t i = 0; i < n; i++) s[i] = (char)(97 + next_random(&seed) % 5);
        s[n] = 0;
        strings[k] = s;
        lens[k] = n;
    }
    int64_t check = 0, pieces = 0;
    for (int pass = 0; pass < 3; pass++) {
        for (int64_t k = 0; k < count; k++) {
            Pieces got = max_num_of_substrings(strings[k], lens[k]);
            for (int64_t q = 0; q < got.len; q++) {
                pieces++;
                check = mix(check, (int64_t)strlen(got.items[q]));
                check = mix(check, (unsigned char)got.items[q][0]);
                free(got.items[q]);
            }
            free(got.items);
        }
    }
    printf("3 passes over 200000 strings of up to 64 letters: %lld substrings, checksum %lld\n",
           (long long)pieces, (long long)check);
    for (int64_t k = 0; k < count; k++) free(strings[k]);
    free(strings);
    free(lens);
    return 0;
}
