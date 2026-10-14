// Benchmark for #553: C mirror of the ★ arm (the shape is always the
// same); see optimal_division.kara. Each answer is a fresh malloc'd
// buffer that grows as it is written, as a String does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *p;
    size_t len, cap;
} Buf;

static void put(Buf *b, const char *s, size_t n) {
    if (b->len + n > b->cap) {
        size_t c = b->cap ? b->cap * 2 : 8;
        while (c < b->len + n) c *= 2;
        b->p = realloc(b->p, c);
        b->cap = c;
    }
    memcpy(b->p + b->len, s, n);
    b->len += n;
}

static Buf optimal_division(const int64_t *nums, int n) {
    Buf out = {0, 0, 0};
    char tmp[24];
    for (int i = 0; i < n; i++) {
        if (i > 0) put(&out, "/", 1);
        if (i == 1 && n > 2) put(&out, "(", 1);
        int k = snprintf(tmp, sizeof tmp, "%lld", (long long)nums[i]);
        put(&out, tmp, (size_t)k);
    }
    if (n > 2) put(&out, ")", 1);
    return out;
}

static int64_t seed = 553;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int count = 2000;
    int64_t nums[2000][10];
    int len[2000];
    for (int g = 0; g < count; g++) {
        len[g] = 1 + (int)(next_random() % 10);
        for (int i = 0; i < len[g]; i++) nums[g][i] = 2 + next_random() % 999;
    }
    int64_t chars = 0, checksum = 0;
    for (int round = 0; round < 500; round++)
        for (int g = 0; g < count; g++) {
            int a = (round * 7 + g) % count;
            Buf t = optimal_division(nums[a], len[a]);
            chars += (int64_t)t.len;
            checksum = (checksum * 31 + (int64_t)t.len + (unsigned char)t.p[t.len / 2]) % 1000000007;
            free(t.p);
        }
    printf("%d arrays, 500 rounds each: %lld characters, checksum %lld\n", count, (long long)chars,
           (long long)checksum);
    return 0;
}
