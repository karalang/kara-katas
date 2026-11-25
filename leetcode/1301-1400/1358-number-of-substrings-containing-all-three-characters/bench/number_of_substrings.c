// LeetCode #1358 bench -- C: where each of a, b and c was last seen; a
// substring ending at i holds all three when it starts at or before the
// earliest of those places.
#include <stdint.h>
#include <stdio.h>

static int64_t number_of_substrings(const uint8_t *s, int64_t n) {
    int64_t last[3] = {-1, -1, -1};
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        last[s[i] - 'a'] = i;
        int64_t m = last[0];
        if (last[1] < m) m = last[1];
        if (last[2] < m) m = last[2];
        count += m + 1;
    }
    return count;
}

static int64_t seed = 1358;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 20 strings of 5 * 10^4 letters, the constraints' most, c drawn one
    // time in 1000 and a and b evenly, built once; then 1000 rounds, each
    // setting one letter of one string, both drawn from the checksum so
    // far, and counting that string's substrings
    static uint8_t texts[20][50000];
    for (int k = 0; k < 20; k++)
        for (int i = 0; i < 50000; i++) {
            int64_t r = next_random() % 1000;
            texts[k][i] = r == 0 ? 'c' : r % 2 == 0 ? 'a' : 'b';
        }
    int64_t check = 0;
    for (int64_t r = 0; r < 1000; r++) {
        int64_t k = check % 20;
        texts[k][(check / 20) % 50000] = (uint8_t)(97 + (check / 7) % 3);
        check = (check * 31 + number_of_substrings(texts[k], 50000) + r) % 1000000007;
    }
    printf("1000 rounds over 20 strings of 5 * 10^4 letters: checksum %lld\n", (long long)check);
    return 0;
}
