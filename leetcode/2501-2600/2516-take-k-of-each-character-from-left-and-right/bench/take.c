// LeetCode #2516: Take K of Each Character From Left and Right -- C mirror
// of the benchmark (take.kara): the same strings, passes, order and
// checksum.
#include <stdint.h>
#include <stdio.h>

#define N 100000

static char strings[40][N];

static int64_t take_characters(const char *s, int64_t n, int64_t k) {
    int64_t total[3] = {0, 0, 0};
    for (int64_t i = 0; i < n; i++) total[s[i] - 'a']++;
    if (total[0] < k || total[1] < k || total[2] < k) return -1;
    int64_t inside[3] = {0, 0, 0};
    int64_t left = 0, longest = 0;
    for (int64_t right = 0; right < n; right++) {
        int c = s[right] - 'a';
        inside[c]++;
        while (total[c] - inside[c] < k) {
            inside[s[left] - 'a']--;
            left++;
        }
        if (right - left + 1 > longest) longest = right - left + 1;
    }
    return n - longest;
}

static int64_t seed = 2516;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    for (int t = 0; t < 40; t++)
        for (int i = 0; i < N; i++) strings[t][i] = (char)('a' + next_random() % 3);
    const int64_t passes = 7;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++)
        for (int t = 0; t < 40; t++)
            check = (check * 31 + take_characters(strings[t], N, check % 30001) + 1 + p) % 1000000007;
    printf("%lld passes over 40 strings of 10^5: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
