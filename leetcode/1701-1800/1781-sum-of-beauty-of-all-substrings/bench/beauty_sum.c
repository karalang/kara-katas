// LeetCode #1781: Sum of Beauty of All Substrings -- the bench in C,
// mirroring beauty_sum.kara: the letters' counts grown from each start.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int beauty_sum(const char *s, long n) {
    int total = 0;
    for (long i = 0; i < n; i++) {
        int counts[26];
        memset(counts, 0, sizeof counts);
        for (long j = i; j < n; j++) {
            counts[s[j] - 'a'] += 1;
            int most = 0;
            int64_t fewest = n;
            for (int c = 0; c < 26; c++) {
                if (counts[c] > 0) {
                    if (counts[c] > most) most = counts[c];
                    if (counts[c] < fewest) fewest = counts[c];
                }
            }
            total += (int)(most - fewest);
        }
    }
    return total;
}

static int64_t seed = 1781;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char words[48][501];
    for (int w = 0; w < 48; w++) {
        int64_t letters = 2 + w % 12 * 2;
        for (int k = 0; k < 500; k++) words[w][k] = (char)(97 + next_random() % letters);
        words[w][500] = 0;
    }
    int64_t check = 0;
    for (int w = 0; w < 48; w++) check = (check * 31 + beauty_sum(words[w], 500)) % 1000000007;
    printf("48 strings of 500 letters: checksum %lld\n", (long long)check);
    return 0;
}
