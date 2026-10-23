// LeetCode #899 bench: the counts arm (rotations compared in place,
// letters counted) on 1,000 strings of 1,000 letters, LeetCode's largest,
// each a random piece of 1 to 4 letters written over and over with one
// letter changed at a random place, so that rotations agree for long
// stretches before they differ. Every string is asked with k = 1, and
// with k = 2 as well. The same algorithm as orderly_queue.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// writes the answer for s (n letters) into out
static void orderly_queue(const char *b, int64_t n, int64_t k, char *out) {
    if (k == 1) {
        int64_t best = 0;
        for (int64_t i = 1; i < n; i++) {
            int64_t d = 0;
            while (d < n && b[(i + d) % n] == b[(best + d) % n]) d++;
            if (d < n && b[(i + d) % n] < b[(best + d) % n]) best = i;
        }
        for (int64_t j = 0; j < n; j++) out[j] = b[(best + j) % n];
        return;
    }
    int64_t count[26] = {0};
    for (int64_t i = 0; i < n; i++) count[b[i] - 97]++;
    int64_t at = 0;
    for (int letter = 0; letter < 26; letter++)
        for (int64_t c = 0; c < count[letter]; c++) out[at++] = (char)(97 + letter);
}

static int64_t seed = 899;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t checksum(const char *s, int64_t n, int64_t check) {
    for (int64_t i = 0; i < n; i++) check = (check * 131 + (unsigned char)s[i]) % 1000000007;
    return check;
}

int main(void) {
    char s[1000], out[1000];
    int64_t check = 0;
    for (int r = 0; r < 1000; r++) {
        int64_t p = 1 + next_random() % 4;
        char piece[4];
        for (int64_t i = 0; i < p; i++) piece[i] = (char)(97 + next_random() % 26);
        int64_t changed = next_random() % 1000;
        char letter = (char)(97 + next_random() % 26);
        for (int64_t i = 0; i < 1000; i++) s[i] = i == changed ? letter : piece[i % p];
        orderly_queue(s, 1000, 1, out);
        check = checksum(out, 1000, check);
        orderly_queue(s, 1000, 2, out);
        check = checksum(out, 1000, check);
    }
    printf("1000 strings of 1000 letters, k = 1 and 2: checksum %lld\n", (long long)check);
    return 0;
}
