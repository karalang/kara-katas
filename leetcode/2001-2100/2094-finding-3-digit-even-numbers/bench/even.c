// LeetCode #2094: Finding 3-Digit Even Numbers -- C mirror of the ★ arm's
// benchmark (even.kara): the same 100000 lists, each answered by the same
// counts and walk over the even numbers from 100 to 998 into a `malloc`'d
// growable array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

typedef struct { int64_t *v; int64_t len, cap; } Vec;

static void push(Vec *a, int64_t x) {
    if (a->len == a->cap) {
        a->cap = a->cap ? a->cap * 2 : 4;
        a->v = realloc(a->v, a->cap * sizeof(int64_t));
    }
    a->v[a->len++] = x;
}

static Vec find_even_numbers(const int64_t *digits, int64_t n) {
    int64_t have[10] = {0};
    for (int64_t i = 0; i < n; i++) have[digits[i]]++;
    Vec found = {0};
    for (int64_t x = 100; x < 1000; x += 2) {
        int64_t need[10] = {0};
        need[x / 100]++;
        need[x / 10 % 10]++;
        need[x % 10]++;
        int ok = 1;
        for (int d = 0; d < 10; d++) {
            if (need[d] > have[d]) {
                ok = 0;
                break;
            }
        }
        if (ok) push(&found, x);
    }
    return found;
}

int main(void) {
    int64_t seed = 2094;
    int64_t count = 0, check = 0;
    const int64_t tops[3] = {10, 6, 4};
    int64_t digits[100];
    for (int t = 0; t < 100000; t++) {
        int64_t len = next_random(&seed) % 98 + 3;
        int64_t top = tops[next_random(&seed) % 3];
        for (int64_t i = 0; i < len; i++) digits[i] = next_random(&seed) % top;
        Vec got = find_even_numbers(digits, len);
        count += got.len;
        for (int64_t i = 0; i < got.len; i++) check = (check * 31 + got.v[i]) % 1000000007;
        free(got.v);
    }
    printf("100000 answers: %lld numbers, checksum %lld\n", (long long)count, (long long)check);
    return 0;
}
