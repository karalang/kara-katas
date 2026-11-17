// LeetCode #2214: Minimum Health to Beat Game -- bench mirror of
// health.kara: the damage summed in one pass with its largest, then the
// sum less what the armor saves on the largest, plus 1.
#include <stdio.h>

static long minimum_health(const long *damage, long n, long armor) {
    long total = 0, worst = 0;
    for (long i = 0; i < n; i++) {
        total += damage[i];
        if (damage[i] > worst) worst = damage[i];
    }
    return total - (worst < armor ? worst : armor) + 1;
}

static long seed = 2214;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

#define G 100
#define N 100000
static long games[G][N];

int main(void) {
    long tops[3] = {10, 1000, 100000};
    for (int g = 0; g < G; g++) {
        // 10^5 levels, the damage up to 10, 1000 and 10^5 in turn
        long top = tops[g % 3];
        for (long i = 0; i < N; i++) games[g][i] = next_random() % (top + 1);
    }
    long check = 0;
    for (int g = 0; g < G; g++)
        for (long a = 0; a < 20; a++) {
            // punch: one level hurts a little more before each answer
            games[g][a * 4999] += 1;
            check = (check * 31 + minimum_health(games[g], N, a * 5000)) % 1000000007;
        }
    printf("100 games of 10^5, 20 armors: checksum %ld\n", check);
    return 0;
}
