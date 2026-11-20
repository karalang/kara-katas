// LeetCode #1700: Number of Students Unable to Eat Lunch -- the bench's C
// mirror: the ★ arm on 50000 random lunches of 100 students, all drawn
// first, each answered 80 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 50000
#define ROUNDS 80
#define N 100

static int32_t count_students(const int32_t *students, const int32_t *sandwiches, int64_t n) {
    int32_t wanting[2] = {0, 0};
    for (int64_t i = 0; i < n; i++) {
        wanting[students[i]]++;
    }
    for (int64_t i = 0; i < n; i++) {
        if (wanting[sandwiches[i]] == 0) {
            break;
        }
        wanting[sandwiches[i]]--;
    }
    return wanting[0] + wanting[1];
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1700;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t *students = malloc((size_t)COUNT * N * sizeof *students);
    int32_t *sandwiches = malloc((size_t)COUNT * N * sizeof *sandwiches);
    for (int64_t c = 0; c < COUNT; c++) {
        int64_t lean = next_random() % 11;
        for (int64_t i = 0; i < N; i++) {
            students[c * N + i] = next_random() % 10 < lean ? 1 : 0;
        }
        for (int64_t i = 0; i < N; i++) {
            sandwiches[c * N + i] = next_random() % 10 < lean ? 1 : 0;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t c = 0; c < COUNT; c++) {
            int64_t answer = count_students(students + c * N, sandwiches + c * N, N);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d lunches of %d students, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)total, (long long)check);
    free(students);
    free(sandwiches);
    return 0;
}
