// LeetCode #1397 bench -- C: the strings built a letter at a time,
// counted by how much of `evil` their end matches and whether they are
// still at s1's prefix and at s2's, the matches stepped through a KMP
// automaton table.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long slot(long long j, int low, int high) {
    return j * 4 + (low ? 2 : 0) + (high ? 1 : 0);
}

static int find_good_strings(int n, const char *s1, const char *s2, const char *evil) {
    const long long modulus = 1000000007;
    long long m = (long long)strlen(evil);
    long long *border = calloc(m, sizeof(long long));
    long long k = 0;
    for (long long i = 1; i < m; i++) {
        while (k > 0 && evil[i] != evil[k]) k = border[k - 1];
        if (evil[i] == evil[k]) k++;
        border[i] = k;
    }
    long long *next = calloc(m * 26, sizeof(long long));
    for (long long j = 0; j < m; j++)
        for (long long c = 0; c < 26; c++) {
            if ((long long)(unsigned char)evil[j] == 97 + c)
                next[j * 26 + c] = j + 1;
            else if (j > 0)
                next[j * 26 + c] = next[border[j - 1] * 26 + c];
        }
    long long *ways = calloc(m * 4, sizeof(long long));
    ways[slot(0, 1, 1)] = 1;
    for (int i = 0; i < n; i++) {
        long long *after = calloc(m * 4, sizeof(long long));
        for (long long j = 0; j < m; j++)
            for (int low = 0; low < 2; low++)
                for (int high = 0; high < 2; high++) {
                    long long w = ways[slot(j, low, high)];
                    if (w == 0) continue;
                    long long first = low ? (long long)s1[i] - 97 : 0;
                    long long last = high ? (long long)s2[i] - 97 : 25;
                    for (long long c = first; c <= last; c++) {
                        long long to = next[j * 26 + c];
                        if (to == m) continue;
                        long long at = slot(to, low && c == first, high && c == last);
                        after[at] = (after[at] + w) % modulus;
                    }
                }
        free(ways);
        ways = after;
    }
    long long total = 0;
    for (long long j = 0; j < m * 4; j++) total = (total + ways[j]) % modulus;
    free(ways);
    free(next);
    free(border);
    return (int)total;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    long long seed = 1397;
    char low[501], high[501], evil[51];
    for (int i = 0; i < 500; i++) low[i] = (char)(97 + next_random(&seed) % 3);
    for (int i = 0; i < 500; i++) high[i] = (char)(120 + next_random(&seed) % 3);
    for (int i = 0; i < 50; i++) evil[i] = (char)(97 + next_random(&seed) % 3);
    low[500] = high[500] = evil[50] = 0;
    long long check = 0;
    for (int r = 0; r < 200; r++) {
        seed = (seed + check) % 2147483648LL;
        long long at = next_random(&seed) % 500;
        low[at] = (char)(97 + next_random(&seed) % 3);
        at = next_random(&seed) % 500;
        high[at] = (char)(120 + next_random(&seed) % 3);
        at = next_random(&seed) % 50;
        evil[at] = (char)(97 + next_random(&seed) % 3);
        check = (check * 131 + find_good_strings(500, low, high, evil)) % 1000000007;
    }
    printf("200 rounds at n = 500, evil of 50 letters: checksum %lld\n", check);
    return 0;
}
