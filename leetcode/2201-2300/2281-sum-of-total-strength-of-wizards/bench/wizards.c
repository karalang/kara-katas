// LeetCode #2281: Sum of Total Strength of Wizards -- the bench, the ★
// arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t total_strength(const int64_t *strength, int64_t n) {
    int64_t *left = malloc(n * sizeof(int64_t));
    int64_t *right = malloc(n * sizeof(int64_t));
    int64_t *stack = malloc(n * sizeof(int64_t));
    int64_t *prefix = malloc((n + 1) * sizeof(int64_t));
    int64_t *twice = malloc((n + 2) * sizeof(int64_t));
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        while (top > 0 && strength[stack[top - 1]] >= strength[i]) top--;
        left[i] = top > 0 ? stack[top - 1] : -1;
        stack[top++] = i;
    }
    top = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        while (top > 0 && strength[stack[top - 1]] > strength[i]) top--;
        right[i] = top > 0 ? stack[top - 1] : n;
        stack[top++] = i;
    }
    prefix[0] = 0;
    for (int64_t i = 0; i < n; i++) prefix[i + 1] = (prefix[i] + strength[i]) % MOD;
    twice[0] = 0;
    for (int64_t i = 0; i < n + 1; i++) twice[i + 1] = (twice[i] + prefix[i]) % MOD;
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t l = left[i], r = right[i];
        int64_t ends = (i - l) * ((twice[r + 1] - twice[i + 1] + MOD) % MOD) % MOD;
        int64_t starts = (r - i) * ((twice[i + 1] - twice[l + 1] + MOD) % MOD) % MOD;
        int64_t groups = (ends - starts + MOD) % MOD;
        total = (total + strength[i] % MOD * groups) % MOD;
    }
    free(left);
    free(right);
    free(stack);
    free(prefix);
    free(twice);
    return total;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2281;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    int64_t *strength = malloc(100000 * sizeof(int64_t));
    for (int t = 0; t < 30; t++) {
        for (int i = 0; i < 100000; i++) {
            int64_t high = next_random();
            strength[i] = (high * 32768 + next_random()) % 1000000000 + 1;
        }
        check = (check * 31 + total_strength(strength, 100000)) % 1000000007;
    }
    free(strength);
    printf("30 armies of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
