// LeetCode #2131: Longest Palindrome by Concatenating Two Letter Words --
// the benchmark, the same algorithm as palindrome.kara; each word two
// bytes in one array per list.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t seed = 2131;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void word(char *w) {
    w[0] = (char)('a' + next_random() % 8);
    w[1] = (char)('a' + next_random() % 8);
}

static int64_t longest_palindrome(const char *words) {
    int64_t count[26 * 26] = {0};
    for (int i = 0; i < N; i++) count[(words[2 * i] - 97) * 26 + (words[2 * i + 1] - 97)]++;
    int64_t length = 0;
    int middle = 0;
    for (int x = 0; x < 26; x++) {
        length += count[x * 26 + x] / 2 * 4;
        if (count[x * 26 + x] % 2 == 1) middle = 1;
        for (int y = x + 1; y < 26; y++) {
            int64_t a = count[x * 26 + y], b = count[y * 26 + x];
            length += (a < b ? a : b) * 4;
        }
    }
    if (middle) length += 2;
    return length;
}

int main(void) {
    char *lists = malloc((size_t)20 * N * 2);
    for (int k = 0; k < 20; k++)
        for (int i = 0; i < N; i++) word(lists + ((size_t)k * N + i) * 2);
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 10; round++) {
        for (int k = 0; k < 20; k++) {
            int64_t hi = next_random();
            int64_t at = (hi * 32768 + next_random()) % N;
            word(lists + ((size_t)k * N + at) * 2);
            int64_t length = longest_palindrome(lists + (size_t)k * N * 2);
            total += length;
            check = (check * 31 + length + round) % 1000000007;
        }
    }
    printf("200 solves: %lld letters in all, checksum %lld\n", (long long)total, (long long)check);
    free(lists);
    return 0;
}
