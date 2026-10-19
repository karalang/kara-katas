// LeetCode 784 — Letter Case Permutation: the bench, in C.
// Mirrors letter_case_permutation.kara: backtracking over the same 64
// strings, every permutation its own heap string.
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **items;
    int64_t len, cap;
} Strings;

static void push(Strings *out, const char *buf, int64_t n) {
    if (out->len == out->cap) {
        out->cap = out->cap ? out->cap * 2 : 4;
        out->items = realloc(out->items, out->cap * sizeof *out->items);
    }
    char *s = malloc(n + 1);
    memcpy(s, buf, n);
    s[n] = 0;
    out->items[out->len++] = s;
}

static void permute(int64_t at, char *buf, int64_t n, Strings *out) {
    if (at == n) {
        push(out, buf, n);
        return;
    }
    char c = buf[at];
    if (isalpha((unsigned char)c)) {
        buf[at] = tolower(c);
        permute(at + 1, buf, n, out);
        buf[at] = toupper(c);
        permute(at + 1, buf, n, out);
        buf[at] = c;
    } else {
        permute(at + 1, buf, n, out);
    }
}

static Strings letter_case_permutation(const char *s) {
    char buf[16];
    int64_t n = strlen(s);
    memcpy(buf, s, n);
    Strings out = {0};
    permute(0, buf, n, &out);
    return out;
}

static int64_t seed = 784;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const char *digits = "0123456789";
    char strings[64][13];
    for (int t = 0; t < 64; t++) {
        int64_t wanted = 6 + next_random() % 6;
        int is_letter[12];
        for (int i = 0; i < 12; i++) is_letter[i] = i < wanted;
        for (int64_t i = 11; i > 0; i--) {
            int64_t j = next_random() % (i + 1);
            int x = is_letter[i];
            is_letter[i] = is_letter[j];
            is_letter[j] = x;
        }
        for (int i = 0; i < 12; i++) {
            if (is_letter[i]) strings[t][i] = letters[next_random() % 52];
            else strings[t][i] = digits[next_random() % 10];
        }
        strings[t][12] = 0;
    }
    const int64_t rounds = 20000;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        Strings all = letter_case_permutation(strings[r % 64]);
        total += all.len;
        for (int64_t i = 0; i < all.len; i++) {
            const unsigned char *b = (const unsigned char *)all.items[i];
            check = (check * 31 + b[0] + 7 * b[11]) % 1000000007;
        }
        for (int64_t i = 0; i < all.len; i++) free(all.items[i]);
        free(all.items);
    }
    printf("%lld rounds of 12-character strings: %lld permutations, checksum %lld\n",
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
