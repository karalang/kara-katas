// LeetCode #2129: Capitalize the Title -- the benchmark, the same
// algorithm as title.kara: each word lowered into a fresh buffer, the
// first letter of a long one raised, the words joined with spaces.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2129;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *capitalize_title(const char *title, size_t n) {
    char *out = malloc(n + 1);
    size_t start = 0;
    for (size_t i = 0; i <= n; i++) {
        if (i < n && title[i] != ' ') continue;
        for (size_t k = start; k < i; k++) {
            char c = title[k];
            if (c >= 'A' && c <= 'Z') c += 32;
            if (k == start && i - start > 2) c -= 32;
            out[k] = c;
        }
        if (i < n) out[i] = ' ';
        start = i + 1;
    }
    out[n] = 0;
    return out;
}

int main(void) {
    static char titles[1000][101];
    static size_t lens[1000];
    for (int k = 0; k < 1000; k++) {
        size_t t = 0;
        for (;;) {
            size_t len = next_random() % 6 + 1;
            if (t + 1 + len > 100) break;
            if (t > 0) titles[k][t++] = ' ';
            for (size_t i = 0; i < len; i++) {
                int64_t c = next_random() % 52;
                titles[k][t++] = (char)(c < 26 ? 97 + c : 39 + c);
            }
        }
        lens[k] = t;
    }
    int64_t capitals = 0, check = 0;
    for (int64_t round = 0; round < 200; round++) {
        for (int k = 0; k < 1000; k++) {
            size_t n = lens[k];
            size_t p = next_random() % n;
            if (titles[k][p] == ' ') p--;
            titles[k][p] ^= 32;
            char *title = malloc(n + 1);
            memcpy(title, titles[k], n);
            title[n] = 0;
            char *answer = capitalize_title(title, n);
            for (size_t i = 0; i < n; i++) {
                unsigned char b = (unsigned char)answer[i];
                if (b >= 65 && b <= 90) capitals++;
                check = (check * 31 + b + round) % 1000000007;
            }
            free(answer);
            free(title);
        }
    }
    printf("200000 titles: %lld capitals, checksum %lld\n", (long long)capitals, (long long)check);
    return 0;
}
