// LeetCode #1701: Average Waiting Time -- the bench's C mirror: the ★ arm
// on 50 random lists of 100000 customers, arrivals and times up to 10^4,
// all drawn first, each answered 60 times.

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 50
#define ROUNDS 60
#define N 100000

static double average_waiting_time(const int32_t (*customers)[2], int64_t n) {
    int64_t finish = 0, waited = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t arrival = customers[i][0];
        finish = (finish > arrival ? finish : arrival) + customers[i][1];
        waited += finish - arrival;
    }
    return (double)waited / (double)n;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1701;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t (*lists)[2] = malloc((size_t)COUNT * N * sizeof *lists);
    for (int c = 0; c < COUNT; c++) {
        int64_t arrival = 0;
        for (int64_t i = 0; i < N; i++) {
            if (next_random() % 10 == 0 && arrival < 9999) {
                arrival++;
            }
            lists[(int64_t)c * N + i][0] = (int32_t)(arrival + 1);
            lists[(int64_t)c * N + i][1] = (int32_t)(next_random() % 10000 + 1);
        }
    }
    double total = 0.0;
    int64_t check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            double answer = average_waiting_time(lists + (int64_t)c * N, N);
            total += answer;
            check = (check * 31 + (int64_t)round(answer * 100000.0) + r) % 1000000007;
        }
    }
    printf("%d lists of %d customers, %d rounds: answers sum to %.5f, checksum %lld\n", COUNT, N, ROUNDS, total, (long long)check);
    free(lists);
    return 0;
}
