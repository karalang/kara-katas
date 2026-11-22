// LeetCode #2801: Count Stepping Numbers in Range -- the bench in C: the
// ★ arm over 400 ranges of 100-digit bounds made mostly of steps, all
// drawn first, then each answered 20 times.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define MOD 1000000007LL
#define COUNT 400
#define M 100

static int64_t seed = 2801;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void number(char *s, int64_t m) {
    int64_t d = next_random() % 9 + 1;
    s[0] = (char)('0' + d);
    for (int64_t i = 1; i < m; i++) {
        int64_t r = next_random() % 10;
        if (r < 8) d = ((r % 2 == 0 && d > 0) || d == 9) ? d - 1 : d + 1;
        else d = r;
        s[i] = (char)('0' + d);
    }
    s[m] = 0;
}

static int64_t walk(const int64_t *digits, int64_t n, int64_t pos, int64_t last, int tight, int started, int64_t memo[][10]) {
    if (pos == n) return started ? 1 : 0;
    int free_ = started && !tight;
    if (free_ && memo[pos][last] >= 0) return memo[pos][last];
    int64_t top = tight ? digits[pos] : 9;
    int64_t ways = 0;
    for (int64_t d = 0; d <= top; d++) {
        int next_tight = tight && d == top;
        if (!started) ways += walk(digits, n, pos + 1, d, next_tight, d > 0, memo);
        else if (d - last == 1 || last - d == 1) ways += walk(digits, n, pos + 1, d, next_tight, 1, memo);
    }
    ways %= MOD;
    if (free_) memo[pos][last] = ways;
    return ways;
}

static int64_t count_up_to(const char *s) {
    int64_t n = (int64_t)strlen(s), digits[M + 1], memo[M + 1][10];
    for (int64_t i = 0; i < n; i++) digits[i] = s[i] - '0';
    for (int64_t i = 0; i < n; i++)
        for (int d = 0; d < 10; d++) memo[i][d] = -1;
    return walk(digits, n, 0, 0, 1, 0, memo);
}

static int steps(const char *s) {
    for (size_t i = 1; s[i]; i++) {
        int diff = s[i] - s[i - 1];
        if (diff != 1 && diff != -1) return 0;
    }
    return 1;
}

static int64_t count_stepping_numbers(const char *low, const char *high) {
    int64_t own = steps(low) ? 1 : 0;
    return ((count_up_to(high) - count_up_to(low) + own) % MOD + MOD) % MOD;
}

static char lows[COUNT][M + 1], highs[COUNT][M + 1];

int main(void) {
    int rounds = 20;
    for (int c = 0; c < COUNT; c++) {
        char a[M + 1], b[M + 1];
        number(a, M);
        number(b, M);
        if (strcmp(a, b) <= 0) { strcpy(lows[c], a); strcpy(highs[c], b); }
        else { strcpy(lows[c], b); strcpy(highs[c], a); }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = count_stepping_numbers(lows[c], highs[c]);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d ranges of 100 digits, %d rounds: counts sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
