// LeetCode #2042: Check if Numbers Are Ascending in a Sentence -- the ★ arm
// in C, the same algorithm and workload as ascending.kara: the sentence
// copied (as the Kāra arm takes its own String), split at its spaces, and
// each token that parses as a whole number compared with the last.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// a token parses when it is non-empty and all digits (an optional sign is
// never written by the workload, whose words are lowercase letters)
static int are_numbers_ascending(const char *sentence) {
    size_t len = strlen(sentence);
    char *s = malloc(len + 1);
    memcpy(s, sentence, len + 1);
    int64_t last = 0;
    size_t start = 0;
    int ok = 1;
    for (size_t i = 0; i <= len; i++) {
        if (i == len || s[i] == ' ') {
            int all_digits = i > start;
            int64_t n = 0;
            for (size_t j = start; j < i; j++) {
                if (s[j] < '0' || s[j] > '9') { all_digits = 0; break; }
                n = n * 10 + (s[j] - '0');
            }
            if (all_digits) {
                if (n <= last) { ok = 0; break; }
                last = n;
            }
            start = i + 1;
        }
    }
    free(s);
    return ok;
}

static int64_t seed = 2042;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *sentence(void) {
    int64_t words = 1 + next_random() % 30;
    int64_t climb = next_random() % 20 + 1;
    int64_t drift = next_random() % 4;
    int64_t last = next_random() % 10 + 1;
    char *out = malloc(512);
    size_t length = 0;
    int numbers = 0;
    out[0] = 0;
    for (int64_t t = 0; t < words + 2; t++) {
        char token[16];
        if (t >= words || next_random() % 3 == 0) {
            last = last + next_random() % (climb + drift + 1) - drift;
            if (last < 1) last = 1;
            if (last > 99) last = 99;
            numbers++;
            snprintf(token, sizeof token, "%lld", (long long)last);
        } else {
            int64_t n = next_random() % 6 + 1;
            for (int64_t c = 0; c < n; c++) token[c] = "abcxyz"[next_random() % 6];
            token[n] = 0;
        }
        size_t tl = strlen(token);
        if (length + tl + 1 > 200 && numbers >= 2) break;
        if (length > 0) out[length - 1] = ' ';  // the last token's NUL becomes a space
        memcpy(out + length, token, tl + 1);
        length += tl + 1;
    }
    return out;
}

int main(void) {
    char *sentences[1000];
    for (int i = 0; i < 1000; i++) sentences[i] = sentence();
    int64_t calls = 0, ascending = 0, check = 0;
    for (int64_t round = 0; round < 1000; round++) {
        for (int64_t i = 0; i < 1000; i++) {
            int answer = are_numbers_ascending(sentences[i]);
            calls++;
            if (answer) {
                ascending++;
                check = (check * 31 + round + i) % 1000000007;
            }
        }
    }
    printf("%lld calls: %lld ascending, checksum %lld\n", (long long)calls, (long long)ascending, (long long)check);
    for (int i = 0; i < 1000; i++) free(sentences[i]);
    return 0;
}
