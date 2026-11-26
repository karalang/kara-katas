// LeetCode #1450 Number of Students Doing Homework at a Given Time: the
// bench, a mirror of busy_student.kara.
#include <stdint.h>
#include <stdio.h>

// each student's start and end side by side, counted when the query falls
// between them
static int busy_student(const int *start_time, const int *end_time, int n, int query_time) {
    int busy = 0;
    for (int i = 0; i < n; i++) {
        if (start_time[i] <= query_time && query_time <= end_time[i]) busy++;
    }
    return busy;
}

int main(void) {
    // 3000 classes of 100 students, the constraints' most, each from a
    // start to an end drawn from 1 to 1000, each class asked at every time
    // from 1 to 1000, the counts folded to a checksum
    int64_t seed = 1450;
    int64_t check = 0;
    for (int r = 0; r < 3000; r++) {
        int start_time[100], end_time[100];
        for (int i = 0; i < 100; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t a = 1 + seed / 65536 % 1000;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t b = 1 + seed / 65536 % 1000;
            start_time[i] = (int)(a < b ? a : b);
            end_time[i] = (int)(a < b ? b : a);
        }
        for (int q = 1; q <= 1000; q++) {
            check = (check * 131 + busy_student(start_time, end_time, 100, q)) % 1000000007;
        }
    }
    printf("3000 classes asked 1000 times: checksum %lld\n", (long long)check);
    return 0;
}
