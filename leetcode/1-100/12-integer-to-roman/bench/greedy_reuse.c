// Diagnostic variant of greedy.c — single buffer allocated ONCE outside
// the K=10M loop and reused per iter. If this comes in dramatically
// faster than greedy.c, the per-iter malloc/free is the dominating cost.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int int_to_roman(int64_t num, int32_t *out) {
    int len = 0;
    int64_t n = num;
    while (n >= 1000) { out[len++] = 'M'; n -= 1000; }
    if    (n >= 900)  { out[len++] = 'C'; out[len++] = 'M'; n -= 900; }
    if    (n >= 500)  { out[len++] = 'D'; n -= 500; }
    if    (n >= 400)  { out[len++] = 'C'; out[len++] = 'D'; n -= 400; }
    while (n >= 100)  { out[len++] = 'C'; n -= 100; }
    if    (n >= 90)   { out[len++] = 'X'; out[len++] = 'C'; n -= 90; }
    if    (n >= 50)   { out[len++] = 'L'; n -= 50; }
    if    (n >= 40)   { out[len++] = 'X'; out[len++] = 'L'; n -= 40; }
    while (n >= 10)   { out[len++] = 'X'; n -= 10; }
    if    (n >= 9)    { out[len++] = 'I'; out[len++] = 'X'; n -= 9; }
    if    (n >= 5)    { out[len++] = 'V'; n -= 5; }
    if    (n >= 4)    { out[len++] = 'I'; out[len++] = 'V'; n -= 4; }
    while (n >= 1)    { out[len++] = 'I'; n -= 1; }
    return len;
}

static int64_t score_roman(const int32_t *r, int len) {
    int64_t s = 0;
    for (int i = 0; i < len; i++) {
        s += (int64_t)r[i];
    }
    return s;
}

int main(void) {
    const int64_t k_iters = 10000000;
    int64_t sum = 0;
    // Single allocation outside the loop. Buffer is reused per iter.
    int32_t *r = (int32_t *)malloc(15 * sizeof(int32_t));
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t raw = k * 2654435769LL + 305419896LL;
        int64_t num = (raw % 3999 + 3999) % 3999 + 1;
        int len = int_to_roman(num, r);
        sum += score_roman(r, len);
    }
    free(r);
    printf("%lld\n", (long long)sum);
    return 0;
}
