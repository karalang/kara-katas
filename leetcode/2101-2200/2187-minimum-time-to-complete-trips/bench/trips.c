// LeetCode #2187: Minimum Time to Complete Trips -- the benchmark's C
// mirror of trips.kara, over a pointer and a length: a binary search
// over the time with the count cut at the total.

#include <stdio.h>
#include <stdlib.h>

static long long trips_by(const long long *time, long long n, long long t, long long total_trips) {
    long long trips = 0;
    for (long long i = 0; i < n; i++) {
        trips += t / time[i];
        if (trips >= total_trips) break;
    }
    return trips;
}

static long long minimum_time(const long long *time, long long n, long long total_trips) {
    long long fastest = time[0];
    for (long long i = 0; i < n; i++) if (time[i] < fastest) fastest = time[i];
    long long lo = 1, hi = fastest * total_trips;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (trips_by(time, n, mid, total_trips) >= total_trips) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static long long seed = 2187;

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
    long long *row = malloc(sizeof(long long) * 1000000);
    for (int i = 0; i < 1000000; i++) row[i] = big_random() % 10000000 + 1;
    long long check = 0;
    for (int r = 0; r < 200; r++) {
        long long start = big_random() % 900001;
        long long trips = big_random() % 10000000 + 1;
        long long t = minimum_time(row + start, 100000, trips);
        check = (check * 31 + t % 1000000007) % 1000000007;
    }
    printf("200 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
