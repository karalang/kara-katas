// LeetCode #1776: Car Fleet II -- the bench in C, mirroring
// get_collision_times.kara: a stack of the cars ahead from the right.
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static double catch_time(const int (*cars)[2], long i, long j) {
    return (double)(cars[j][0] - cars[i][0]) / (double)(cars[i][1] - cars[j][1]);
}

static double *get_collision_times(const int (*cars)[2], long n) {
    double *answer = malloc(sizeof(double) * n);
    long *stack = malloc(sizeof(long) * n);
    long top = 0;
    for (long i = 0; i < n; i++) answer[i] = -1.0;
    for (long i = n - 1; i >= 0; i--) {
        while (top > 0) {
            long j = stack[top - 1];
            if (cars[i][1] <= cars[j][1] || (answer[j] > 0.0 && catch_time(cars, i, j) >= answer[j])) {
                top--;
            } else {
                break;
            }
        }
        if (top > 0) answer[i] = catch_time(cars, i, stack[top - 1]);
        stack[top++] = i;
    }
    free(stack);
    return answer;
}

static int64_t seed = 1776;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int (*lists[20])[2];
    for (int l = 0; l < 20; l++) {
        int64_t fastest = l % 2 == 0 ? 1000000 : 100;
        lists[l] = malloc(sizeof(int[2]) * 100000);
        int64_t position = 0;
        for (int k = 0; k < 100000; k++) {
            position += 1 + next_random() % 10;
            int64_t speed = 1 + next_random() % fastest;
            lists[l][k][0] = (int)position;
            lists[l][k][1] = (int)speed;
        }
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 200; call++) {
        double *answer = get_collision_times((const int (*)[2])lists[(check + call) % 20], 100000);
        double t = answer[check % 100000];
        check = (check * 31 + (int64_t)floor(t * 100000.0 + 0.5) + 100001) % 1000000007;
        free(answer);
    }
    printf("200 calls over 20 lists: checksum %lld\n", (long long)check);
    for (int l = 0; l < 20; l++) free(lists[l]);
    return 0;
}
