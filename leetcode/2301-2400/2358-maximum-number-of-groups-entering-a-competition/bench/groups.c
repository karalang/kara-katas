// LeetCode #2358: Maximum Number of Groups Entering a Competition -- the
// bench, the ★ arm in C: group sizes 1, 2, 3, ... added while the next
// still fits in the class.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t maximum_groups(const int64_t *grades, int64_t n) {
    (void)grades;
    int64_t k = 0;
    int64_t used = 0;
    while (used + k + 1 <= n) {
        k++;
        used += k;
    }
    return k;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // class a holds 10^4 (a + 1) - a students graded 1 to 10^5
    int64_t seed = 2358;
    int64_t *classes[10];
    int64_t sizes[10];
    for (int64_t a = 0; a < 10; a++) {
        sizes[a] = 10000 * (a + 1) - a;
        classes[a] = malloc(sizes[a] * sizeof(int64_t));
        for (int64_t i = 0; i < sizes[a]; i++) {
            classes[a][i] = 1 + next_random(&seed) % 100000;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20000; p++) {
        for (int a = 0; a < 10; a++) {
            check = (check * 31 + maximum_groups(classes[a], sizes[a]) + p) % 1000000007;
        }
    }
    printf("20000 passes over 10 classes: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(classes[a]);
    }
    return 0;
}
