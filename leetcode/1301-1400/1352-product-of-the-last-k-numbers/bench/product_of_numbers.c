// LeetCode #1352 bench -- C: the running products since the last zero,
// after a leading 1.
#include <stdio.h>
#include <stdlib.h>

static long long *prefix;
static long len, cap;

static void add(int num) {
    if (num == 0) {
        len = 1;
        prefix[0] = 1;
        return;
    }
    if (len == cap) {
        cap *= 2;
        prefix = realloc(prefix, cap * sizeof(long long));
    }
    prefix[len] = prefix[len - 1] * num;
    len++;
}

static int get_product(long k) {
    if (k >= len) return 0;
    return (int)(prefix[len - 1] / prefix[len - 1 - k]);
}

int main(void) {
    cap = 16;
    prefix = malloc(cap * sizeof(long long));
    prefix[0] = 1;
    len = 1;
    long long seed = 1352, since = 1, check = 0;
    for (long long r = 0; r < 10000000; r++) {
        long long num = 1;
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        if ((seed / 65536) % 1000 == 0) {
            num = 0;
            since = 1;
        } else {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            if ((seed / 65536) % 20 == 0) {
                seed = (seed * 1103515245 + 12345) % 2147483648LL;
                num = 2 + (seed / 65536) % 99;
            }
            if (since * num >= 2147483648LL) num = 1;
            since *= num;
        }
        add((int)num);
        long long lim = r + 1 < 50000 ? r + 1 : 50000;
        long long k = 1 + check % lim;
        check = (check * 31 + get_product(k) + r) % 1000000007;
    }
    printf("10000000 rounds: checksum %lld\n", check);
    free(prefix);
    return 0;
}
