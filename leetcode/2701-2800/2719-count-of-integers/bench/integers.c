// LeetCode #2719: Count of Integers -- the bench (integers.kara in C): the
// good numbers up to each bound by a digit-by-digit recursion, a free
// place's count remembered by place and digit sum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007LL

typedef struct {
    const int64_t *digits;
    int64_t n, min_sum, max_sum;
    int64_t *memo; /* n rows of max_sum + 1 */
} Walk;

static int64_t walk(const Walk *w, int64_t place, int64_t sum, int tight) {
    if (sum > w->max_sum) return 0;
    if (place == w->n) return sum >= w->min_sum ? 1 : 0;
    int64_t *slot = &w->memo[place * (w->max_sum + 1) + sum];
    if (!tight && *slot >= 0) return *slot;
    int64_t top = tight ? w->digits[place] : 9;
    int64_t ways = 0;
    for (int64_t d = 0; d <= top; d++) ways = (ways + walk(w, place + 1, sum + d, tight && d == top)) % MOD;
    if (!tight) *slot = ways;
    return ways;
}

static int64_t good_up_to(const char *bound, int64_t min_sum, int64_t max_sum) {
    int64_t n = (int64_t)strlen(bound);
    int64_t *digits = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t i = 0; i < n; i++) digits[i] = bound[i] - '0';
    int64_t *memo = malloc(sizeof(int64_t) * (size_t)(n * (max_sum + 1)));
    for (int64_t i = 0; i < n * (max_sum + 1); i++) memo[i] = -1;
    Walk w = {digits, n, min_sum, max_sum, memo};
    int64_t ways = walk(&w, 0, 0, 1);
    free(digits);
    free(memo);
    return ways;
}

static int64_t count(const char *num1, const char *num2, int64_t min_sum, int64_t max_sum) {
    int64_t own = 0;
    for (const char *p = num1; *p; p++) own += *p - '0';
    int64_t itself = min_sum <= own && own <= max_sum ? 1 : 0;
    return (good_up_to(num2, min_sum, max_sum) - good_up_to(num1, min_sum, max_sum) + itself + MOD) % MOD;
}

static int64_t seed = 2719;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { RANGES = 300, ROUNDS = 10 };
    static char num1[RANGES][23], num2[RANGES][23];
    static int64_t low[RANGES], high[RANGES];
    for (int k = 0; k < RANGES; k++) {
        num1[k][0] = (char)('1' + next_random() % 4);
        num2[k][0] = (char)('5' + next_random() % 5);
        for (int i = 1; i < 22; i++) {
            num1[k][i] = (char)('0' + next_random() % 10);
            num2[k][i] = (char)('0' + next_random() % 10);
        }
        num1[k][22] = num2[k][22] = 0;
        low[k] = next_random() % 400 + 1;
        high[k] = low[k] + next_random() % (401 - low[k]);
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int k = 0; k < RANGES; k++) {
            int64_t found = count(num1[k], num2[k], low[k], high[k]);
            sum += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    printf("%d ranges of 22 digits, %d rounds: counts mod p sum to %lld, checksum %lld\n", RANGES, ROUNDS, (long long)sum, (long long)check);
    return 0;
}
