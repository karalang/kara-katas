// LeetCode #1208 bench, in C: the ★ arm (a window over the letters, widened
// one letter a step and shrunk from the left while it costs more than the
// budget) on 16 pairs of strings of 100000 letters drawn once, then 10
// rounds over the pairs with the budgets 0, 1000, 100000 and 1000000,
// every answer folded into a checksum.

#include <stdio.h>
#include <stdlib.h>

#define PAIRS 16
#define LEN 100000

static long long seed = 1208;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long equal_substring(const char *a, const char *b, int n, long long max_cost) {
    long long best = 0, cost = 0;
    int left = 0;
    for (int right = 0; right < n; right++) {
        cost += llabs((long long)a[right] - b[right]);
        while (cost > max_cost) {
            cost -= llabs((long long)a[left] - b[left]);
            left++;
        }
        if (right - left + 1 > best) best = right - left + 1;
    }
    return best;
}

int main(void) {
    static char s[PAIRS][LEN], t[PAIRS][LEN];
    for (int p = 0; p < PAIRS; p++) {
        long long spread = 2;
        for (int i = 0; i < LEN; i++) {
            if (i % 1000 == 0) spread = next_random() % 2 == 0 ? 2 : 25;
            long long x = next_random() % 26;
            long long y = (x + next_random() % (spread + 1)) % 26;
            s[p][i] = (char)('a' + x);
            t[p][i] = (char)('a' + y);
        }
    }
    const long long budgets[4] = {0, 1000, 100000, 1000000};
    long long check = 0;
    for (int round = 0; round < 10; round++)
        for (int p = 0; p < PAIRS; p++)
            for (int k = 0; k < 4; k++)
                check = (check * 131 + equal_substring(s[p], t[p], LEN, budgets[k]) + round) % 1000000007;
    printf("10 rounds over 16 pairs of 100000 letters: checksum %lld\n", check);
    return 0;
}
