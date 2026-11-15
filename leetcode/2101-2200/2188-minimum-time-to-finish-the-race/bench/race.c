// LeetCode #2188: Minimum Time to Finish the Race -- the benchmark's C
// mirror of race.kara, over a pointer to the window's (f, r) pairs and a
// length: the runs on one tire, then the laps bottom up.

#include <stdio.h>
#include <stdlib.h>

static long long minimum_finish_time(const long long (*tires)[2], long long n, long long change_time, long long num_laps, long long *best) {
    long long run[64];
    long long run_len = 1;
    run[0] = 0;
    for (long long i = 0; i < n; i++) {
        long long f = tires[i][0], r = tires[i][1];
        long long lap = f, sum = 0, k = 1;
        while (k <= num_laps && lap <= change_time + f) {
            sum += lap;
            if (k == run_len) run[run_len++] = sum;
            else if (sum < run[k]) run[k] = sum;
            lap *= r;
            k++;
        }
    }
    best[0] = 0;
    for (long long m = 1; m <= num_laps; m++) {
        long long least = run[1] * m + change_time * (m - 1);
        for (long long k = 1; k < run_len && k <= m; k++) {
            long long pit = k == m ? 0 : change_time;
            long long t = best[m - k] + pit + run[k];
            if (t < least) least = t;
        }
        best[m] = least;
    }
    return best[num_laps];
}

static long long seed = 2188;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long big_random(void) {
    long long a = next_random();
    long long b = next_random();
    return a * 32768 + b;
}

int main(void) {
    long long (*row)[2] = malloc(sizeof(long long[2]) * 100000);
    for (int i = 0; i < 100000; i++) {
        row[i][0] = big_random() % 100 + 1;
        row[i][1] = next_random() % 4 + 2;
    }
    long long check = 0;
    for (int s = 0; s < 5000; s++) {
        long long start = big_random() % 99901;
        long long change_time = big_random() % 100000 + 1;
        long long num_laps = 1000;
        long long *best = malloc(sizeof(long long) * (num_laps + 1));
        long long t = minimum_finish_time(row + start, 100, change_time, num_laps, best);
        free(best);
        check = (check * 31 + t % 1000000007) % 1000000007;
    }
    printf("5000 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
