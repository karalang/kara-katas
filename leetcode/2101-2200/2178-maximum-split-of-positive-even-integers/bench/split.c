// LeetCode #2178: Maximum Split of Positive Even Integers -- the
// benchmark's C mirror of split.kara, the parts in a growing heap array.

#include <stdio.h>
#include <stdlib.h>

static long long *maximum_even_split(long long final_sum, long long *len) {
    long long cap = 16, n = 0;
    long long *parts = malloc(cap * sizeof(long long));
    if (final_sum % 2 != 0) {
        *len = 0;
        return parts;
    }
    long long left = final_sum, next = 2;
    while (left >= next) {
        if (n == cap) {
            cap *= 2;
            parts = realloc(parts, cap * sizeof(long long));
        }
        parts[n++] = next;
        left -= next;
        next += 2;
    }
    parts[n - 1] += left;
    *len = n;
    return parts;
}

static long long seed = 2178;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long parts_in_all = 0, check = 0;
    for (int r = 0; r < 400; r++) {
        long long a = next_random();
        long long b = next_random();
        long long c = next_random();
        long long final_sum = ((a * 32768 + b) * 32768 + c) % 10000000000LL + 1;
        long long len;
        long long *parts = maximum_even_split(final_sum, &len);
        parts_in_all += len;
        for (long long i = 0; i < len; i++) check = (check * 31 + parts[i]) % 1000000007;
        free(parts);
    }
    printf("400 solves: %lld parts, checksum %lld\n", parts_in_all, check);
    return 0;
}
