// Benchmark for #555: C mirror of the ★ arm (every cut, the rest at its
// best); see split_concatenated_strings.kara. Each candidate is a fresh
// malloc'd string, compared with the best so far and kept or freed, as
// a String is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

typedef struct {
    char *p;
    size_t len;
} Str;

// Compare as byte strings, the shorter first on a common prefix.
static int greater(Str a, Str b) {
    size_t m = a.len < b.len ? a.len : b.len;
    int c = memcmp(a.p, b.p, m);
    return c != 0 ? c > 0 : a.len > b.len;
}

static Str reversed(Str s) {
    Str r = {malloc(s.len + 1), s.len};
    for (size_t i = 0; i < s.len; i++) r.p[i] = s.p[s.len - 1 - i];
    return r;
}

static Str split_loop(const Str *strs, size_t n) {
    Str *larger = malloc(n * sizeof(Str));
    size_t total = 0;
    for (size_t i = 0; i < n; i++) {
        Str r = reversed(strs[i]);
        if (greater(r, strs[i])) {
            larger[i] = r;
        } else {
            free(r.p);
            larger[i].p = malloc(strs[i].len + 1);
            memcpy(larger[i].p, strs[i].p, strs[i].len);
            larger[i].len = strs[i].len;
        }
        total += strs[i].len;
    }
    Str answer = {malloc(1), 0};
    char *middle = malloc(total + 1);
    for (size_t i = 0; i < n; i++) {
        size_t m = 0;
        for (size_t j = 1; j < n; j++) {
            Str s = larger[(i + j) % n];
            memcpy(middle + m, s.p, s.len);
            m += s.len;
        }
        Str ways[2] = {strs[i], reversed(strs[i])};
        for (int w = 0; w < 2; w++) {
            Str t = ways[w];
            for (size_t k = 0; k < t.len; k++) {
                Str cand = {malloc(t.len + m + 1), t.len + m};
                memcpy(cand.p, t.p + k, t.len - k);
                memcpy(cand.p + t.len - k, middle, m);
                memcpy(cand.p + t.len - k + m, t.p, k);
                if (greater(cand, answer)) {
                    free(answer.p);
                    answer = cand;
                } else {
                    free(cand.p);
                }
            }
        }
        free(ways[1].p);
    }
    free(middle);
    for (size_t i = 0; i < n; i++) free(larger[i].p);
    free(larger);
    return answer;
}

int main(void) {
    const int count = 100;
    int64_t seed = 555;
    Str *lists[100];
    size_t sizes[100];
    long strings = 0;
    for (int g = 0; g < count; g++) {
        int64_t alphabet = 2 + next_random(&seed) % 25;
        size_t cap = 16, n = 0;
        Str *strs = malloc(cap * sizeof(Str));
        int64_t left = 1000;
        while (left > 0) {
            int64_t length = 1 + next_random(&seed) % 40;
            if (length > left) length = left;
            Str s = {malloc((size_t)length + 1), (size_t)length};
            for (int64_t k = 0; k < length; k++) s.p[k] = (char)('a' + next_random(&seed) % alphabet);
            if (n == cap) strs = realloc(strs, (cap *= 2) * sizeof(Str));
            strs[n++] = s;
            left -= length;
        }
        strings += (long)n;
        lists[g] = strs;
        sizes[g] = n;
    }
    int64_t checksum = 0;
    for (int round = 0; round < 30; round++) {
        for (int g = 0; g < count; g++) {
            int at = (round * 7 + g) % count;
            Str got = split_loop(lists[at], sizes[at]);
            unsigned char *b = (unsigned char *)got.p;
            checksum = (checksum * 31 + (int64_t)got.len + (int64_t)b[0] * 7 + (int64_t)b[got.len / 2]) % 1000000007;
            free(got.p);
        }
    }
    printf("%d lists, %ld strings, 30 rounds each: checksum %lld\n", count, strings, (long long)checksum);
    return 0;
}
