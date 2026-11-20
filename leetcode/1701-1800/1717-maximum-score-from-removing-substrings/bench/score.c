// LeetCode #1717: Maximum Score From Removing Substrings -- the C mirror of
// the bench (score.kara): the pair worth more removed first with a stack,
// then the other pair from what is left, on 20 random strings of 100000
// letters, each answered 100 times. The letters are held 4 bytes each, as a
// Kāra `char`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// keeps the letters of `chars` not paired into `kept`, returning how many
static long remove_pairs(const uint32_t *chars, long n, uint32_t first, uint32_t second, int points, uint32_t *kept, int *gained) {
    long len = 0;
    *gained = 0;
    for (long i = 0; i < n; i++) {
        uint32_t c = chars[i];
        if (c == second && len > 0 && kept[len - 1] == first) {
            len--;
            *gained += points;
        } else {
            kept[len++] = c;
        }
    }
    return len;
}

static int maximum_gain(const char *s, long n, int x, int y) {
    uint32_t *chars = malloc(sizeof(uint32_t) * n);
    for (long i = 0; i < n; i++) {
        chars[i] = (unsigned char)s[i];
    }
    uint32_t first = 'b', second = 'a';
    int more = y, less = x;
    if (x >= y) {
        first = 'a';
        second = 'b';
        more = x;
        less = y;
    }
    uint32_t *rest = malloc(sizeof(uint32_t) * n);
    uint32_t *last = malloc(sizeof(uint32_t) * n);
    int a, b;
    long kept = remove_pairs(chars, n, first, second, more, rest, &a);
    remove_pairs(rest, kept, second, first, less, last, &b);
    free(chars);
    free(rest);
    free(last);
    return a + b;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 20;
    const long long rounds = 100;
    const long n = 100000;
    long long seed = 1717;
    char *strings = malloc(count * n);
    int xs[20], ys[20];
    for (int p = 0; p < count; p++) {
        for (long i = 0; i < n; i++) {
            long long r = next_random(&seed) % 200;
            strings[p * n + i] = r < 2 ? 'c' : (r % 2 == 0 ? 'a' : 'b');
        }
        xs[p] = (int)(next_random(&seed) % 10000 + 1);
        ys[p] = (int)(next_random(&seed) % 10000 + 1);
    }
    long long sum = 0;
    long long check = 0;
    for (long long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            long long answer = maximum_gain(strings + p * n, n, xs[p], ys[p]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d strings of %ld letters, %lld rounds: answers sum to %lld, checksum %lld\n", count, n, rounds, sum, check);
    free(strings);
    return 0;
}
