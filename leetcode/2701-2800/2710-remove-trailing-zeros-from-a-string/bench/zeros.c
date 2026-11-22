// LeetCode #2710: Remove Trailing Zeros From a String -- the bench
// (zeros.kara in C): an index walks back over the zeros, and the digits
// before it are copied out.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *remove_trailing_zeros(const char *num, int n, int *out_len) {
    int end = n;
    while (num[end - 1] == '0') end -= 1;
    char *out = malloc(end + 1);
    memcpy(out, num, end);
    out[end] = 0;
    *out_len = end;
    return out;
}

static int64_t seed = 2710;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 20000, rounds = 20;
    char *numbers = malloc((size_t)count * 1000);
    for (int c = 0; c < count; c++) {
        char *num = numbers + (size_t)c * 1000;
        int zeros = (int)(next_random() % 1000);
        num[0] = (char)('1' + next_random() % 9);
        for (int i = 1; i < 1000 - zeros; i++) num[i] = (char)('0' + next_random() % 10);
        for (int i = 1000 - zeros; i < 1000; i++) num[i] = '0';
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            int kept;
            char *out = remove_trailing_zeros(numbers + (size_t)c * 1000, 1000, &kept);
            sum += kept;
            check = (check * 31 + kept + (unsigned char)out[kept - 1] + r) % 1000000007;
            free(out);
        }
    }
    printf("%d numbers of 1000 digits, %d rounds: %lld digits kept, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(numbers);
    return 0;
}
