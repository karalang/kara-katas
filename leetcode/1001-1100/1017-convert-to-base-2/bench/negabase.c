// LeetCode #1017: Convert to Base -2 -- bench
// Mirrors negabase.kara; see ../README.md § Benchmarks.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// n's base -2 form, a fresh string the caller frees
static char *base_neg2(int64_t n) {
    if (n == 0) {
        char *zero = malloc(2);
        strcpy(zero, "0");
        return zero;
    }
    char rev[72];
    int k = 0;
    int64_t rest = n;
    while (rest != 0) {
        int64_t bit = rest & 1;
        rev[k++] = bit == 1 ? '1' : '0';
        rest = (rest - bit) / -2;
    }
    char *form = malloc((size_t)k + 1);
    for (int i = 0; i < k; i++) {
        form[i] = rev[k - 1 - i];
    }
    form[k] = '\0';
    return form;
}

int main(void) {
    int64_t most = 3000000;
    int64_t digits = 0;
    int64_t check = 0;
    for (int64_t n = 0; n < most + 1; n++) {
        char *form = base_neg2(n);
        int64_t len = (int64_t)strlen(form);
        digits += len;
        for (int64_t i = 0; i < len; i++) {
            check = (check * 3 + (form[i] == '1' ? 2 : 1)) % 1000000007;
        }
        check = (check * 3) % 1000000007;
        free(form);
    }
    printf("n = 0..%lld: %lld digits, checksum %lld\n", (long long)most, (long long)digits,
           (long long)check);
    return 0;
}
