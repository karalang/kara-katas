// LeetCode #880 bench: C mirror of decode_at_index.kara (the ★ arm, the
// tape's length, then back from the end) on the same 1,000,000 queries.

#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int is_digit(char c) {
    return c >= '0' && c <= '9';
}

static char decode_at_index(const char *s, int64_t k) {
    int64_t n = (int64_t)strlen(s);
    int64_t size = 0;
    for (int64_t i = 0; i < n; i++) {
        if (is_digit(s[i])) {
            size *= s[i] - '0';
        } else {
            size += 1;
        }
    }
    for (int64_t i = n - 1;; i--) {
        k %= size;
        if (k == 0 && !is_digit(s[i])) {
            return s[i];
        }
        if (is_digit(s[i])) {
            size /= s[i] - '0';
        } else {
            size -= 1;
        }
    }
}

static int64_t seed = 880;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t up_to(int64_t limit) {
    int64_t x = next_random();
    int64_t y = next_random();
    return (x * 32768 + y) % limit + 1;
}

static int64_t encoded(char *s, int64_t length) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    const int64_t bound = 1000000000000000000LL;
    int64_t size = 0, at = 0;
    for (int64_t i = 0; i < length; i++) {
        int64_t d = next_random() % 8 + 2;
        if (i > 0 && next_random() % 3 == 0 && size * d <= bound) {
            s[at++] = (char)('0' + d);
            size *= d;
        } else if (size < bound) {
            s[at++] = letters[next_random() % 26];
            size += 1;
        }
    }
    s[at] = '\0';
    return size;
}

static char strings[1000][101];
static int64_t sizes[1000];

int main(void) {
    for (int j = 0; j < 1000; j++) {
        int64_t length = next_random() % 99 + 2;
        sizes[j] = encoded(strings[j], length);
    }
    int64_t total = 0, check = 0;
    for (int q = 0; q < 1000000; q++) {
        int j = q % 1000;
        int64_t k = up_to(sizes[j] < 1000000000 ? sizes[j] : 1000000000);
        int64_t answer = decode_at_index(strings[j], k);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    printf("1000000 queries over 1000 strings: letters sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
