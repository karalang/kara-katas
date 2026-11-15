// LeetCode #1165: Single-Row Keyboard -- C mirror of the Kāra ★ arm: each
// letter's place in a table of 26, then the moves summed from place 0.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t calculate_time(const char *keyboard, const char *word, int64_t n) {
    int64_t place[26] = {0};
    for (int64_t i = 0; i < 26; i++) place[keyboard[i] - 'a'] = i;
    int64_t at = 0, time = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t next = place[word[i] - 'a'];
        time += llabs(next - at);
        at = next;
    }
    return time;
}

static int64_t seed = 1165;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char keyboards[16][26];
static char words[16][10000];

int main(void) {
    for (int k = 0; k < 16; k++) {
        char b[26];
        for (int i = 0; i < 26; i++) b[i] = 'a' + i;
        for (int i = 25; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            char t = b[i]; b[i] = b[j]; b[j] = t;
        }
        for (int i = 0; i < 26; i++) keyboards[k][i] = b[i];
        for (int i = 0; i < 10000; i++) words[k][i] = 'a' + next_random() % 26;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < 5000; r++)
        for (int k = 0; k < 16; k++) {
            int64_t from = next_random() % 5000;
            int64_t t = calculate_time(keyboards[k], words[k] + from, 10000 - from);
            total += t;
            check = (check * 31 + t) % 1000000007;
        }
    printf("5000 rounds over 16 words of 10^4 letters: total %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
