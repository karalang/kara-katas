// LeetCode 753 — Cracking the Safe, bench: the ★ arm (an Euler circuit
// by Hierholzer's method), mirrored from crack_safe.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static char *crack_safe(int64_t n, int64_t k, int64_t *len) {
    int64_t nodes = 1;
    for (int64_t i = 0; i < n - 1; i++) nodes *= k;
    int64_t *used = calloc(nodes, sizeof *used);
    int64_t cap = nodes * k + 1;
    int64_t *snode = malloc(cap * sizeof *snode), *sdig = malloc(cap * sizeof *sdig);
    int64_t *digits = malloc(cap * sizeof *digits);
    int64_t top = 0, nd = 0;
    snode[top] = 0; sdig[top] = -1; top++;
    while (top > 0) {
        int64_t node = snode[top - 1], digit = sdig[top - 1];
        if (used[node] < k) {
            int64_t d = used[node];
            used[node] += 1;
            snode[top] = (node * k + d) % nodes; sdig[top] = d; top++;
        } else {
            top--;
            if (digit >= 0) digits[nd++] = digit;
        }
    }
    char *out = malloc(n - 1 + nd + 1);
    int64_t o = 0;
    for (int64_t i = 0; i < n - 1; i++) out[o++] = '0';
    for (int64_t i = nd - 1; i >= 0; i--) out[o++] = (char)('0' + digits[i]);
    out[o] = 0;
    free(used); free(snode); free(sdig); free(digits);
    *len = o;
    return out;
}

int main(void) {
    int64_t rounds = 2000, safes = 0, digits = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int64_t n = 1; n < 5; n++)
            for (int64_t k = 1; k < 11; k++) {
                int64_t total = 1;
                for (int64_t i = 0; i < n; i++) total *= k;
                if (total <= 4096) {
                    safes++;
                    int64_t len;
                    char *text = crack_safe(n, k, &len);
                    digits += len;
                    for (int64_t i = 0; i < len; i++) check = (check * 31 + (unsigned char)text[i]) % 1000000007;
                    free(text);
                }
            }
    printf("%lld safes: %lld digits in all, checksum %lld\n", (long long)safes, (long long)digits, (long long)check);
    return 0;
}
