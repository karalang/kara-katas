// LeetCode #2709: Greatest Common Divisor Traversal -- the bench
// (traversal.kara in C): a smallest-prime-factor sieve, and each index
// joined in a union-find to the first index seen with each of its
// primes.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find(int64_t *parent, int64_t a) {
    while (parent[a] != a) {
        parent[a] = parent[parent[a]];
        a = parent[a];
    }
    return a;
}

static bool can_traverse_all_pairs(const int64_t *nums, int64_t n) {
    if (n == 1) return true;
    int64_t top = nums[0];
    for (int64_t i = 1; i < n; i++) if (nums[i] > top) top = nums[i];
    int64_t *spf = malloc(sizeof(int64_t) * (top + 1));
    for (int64_t i = 0; i <= top; i++) spf[i] = i;
    for (int64_t p = 2; p * p <= top; p++) {
        if (spf[p] == p) {
            for (int64_t m = p * p; m <= top; m += p) {
                if (spf[m] == m) spf[m] = p;
            }
        }
    }
    int64_t *parent = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) parent[i] = i;
    int64_t *first = malloc(sizeof(int64_t) * (top + 1));
    for (int64_t i = 0; i <= top; i++) first[i] = -1;
    int64_t sets = n;
    bool ok = true;
    for (int64_t i = 0; i < n && ok; i++) {
        int64_t rest = nums[i];
        if (rest == 1) {
            ok = false;
            break;
        }
        while (rest > 1) {
            int64_t q = spf[rest];
            while (rest % q == 0) rest /= q;
            if (first[q] < 0) {
                first[q] = i;
            } else {
                int64_t a = find(parent, i), b = find(parent, first[q]);
                if (a != b) {
                    parent[a] = b;
                    sets -= 1;
                }
            }
        }
    }
    free(spf);
    free(parent);
    free(first);
    return ok && sets == 1;
}

static int64_t seed = 2709;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int arrays = 20, n = 100000, rounds = 5;
    static const int64_t small[4] = {2, 3, 5, 7};
    int64_t *all = malloc(sizeof(int64_t) * arrays * n);
    for (int a = 0; a < arrays; a++) {
        for (int i = 0; i < n; i++) {
            if (a % 2 == 0) {
                int64_t p = small[next_random() % 4];
                all[a * n + i] = p * (wide() % 14285 + 1);
            } else {
                all[a * n + i] = wide() % 99999 + 2;
            }
        }
    }
    int64_t yes = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int a = 0; a < arrays; a++) {
            bool can = can_traverse_all_pairs(all + a * n, n);
            if (can) yes += 1;
            check = (check * 31 + (can ? 2 : 1) + r) % 1000000007;
        }
    }
    printf("%d arrays of %d numbers up to 100000, %d rounds: %lld traversable, checksum %lld\n", arrays, n, rounds, (long long)yes, (long long)check);
    free(all);
    return 0;
}
