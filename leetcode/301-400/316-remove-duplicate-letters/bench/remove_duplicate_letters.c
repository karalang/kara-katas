// Benchmark lane for LeetCode 316 — C mirror of bench/remove_duplicate_letters.kara.
// Generate N drifting letters once, then PASSES monotone-stack passes (record
// each letter's last occurrence, then skip placed letters and pop larger tops
// that still have a later copy), each after overwriting one position chosen
// from the checksum.
#include <stdio.h>
#include <stdlib.h>

#define N 4000000
#define PASSES 100
#define MASK 1073741823LL

static long long lcg(long long s) {
    return (s * 1103515245LL + 12345LL) & 0x7fffffffLL;
}

// Writes the answer into out (capacity >= 26), returns its length.
static int remove_duplicate_letters(const unsigned char *bs, long long n, unsigned char *out) {
    long long last[26];
    int on_stack[26];
    for (int k = 0; k < 26; k++) { last[k] = -1; on_stack[k] = 0; }
    for (long long i = 0; i < n; i++) last[bs[i] - 'a'] = i;
    int top = 0;
    for (long long i = 0; i < n; i++) {
        unsigned char c = bs[i];
        int ci = c - 'a';
        if (on_stack[ci]) continue;
        while (top > 0) {
            unsigned char t = out[top - 1];
            if (t > c && last[t - 'a'] > i) {
                top--;
                on_stack[t - 'a'] = 0;
            } else {
                break;
            }
        }
        out[top++] = c;
        on_stack[ci] = 1;
    }
    return top;
}

int main(void) {
    long long seed = 316;
    unsigned char *text = malloc(N);
    long long cur = 25;
    for (long long i = 0; i < N; i++) {
        seed = lcg(seed);
        long long r = seed / 65536;
        if (r % 4 != 0) {
            cur -= 1;
            if (cur < 0) cur = 25;
        } else {
            cur = r % 26;
        }
        text[i] = (unsigned char)(cur + 'a');
    }

    long long checksum = 0;
    unsigned char out[26];
    for (int pass = 0; pass < PASSES; pass++) {
        long long i = checksum % N;
        unsigned char letter = (unsigned char)((checksum * 7 + 13) % 26);
        unsigned char saved = text[i];
        text[i] = (unsigned char)(letter + 'a');
        int len = remove_duplicate_letters(text, N, out);
        long long fold = 0;
        for (int k = 0; k < len; k++) fold = (fold * 131 + out[k]) & MASK;
        checksum = (checksum * 31 + fold + len) & MASK;
        text[i] = saved;
    }
    printf("checksum %lld\n", checksum);
    free(text);
    return 0;
}
