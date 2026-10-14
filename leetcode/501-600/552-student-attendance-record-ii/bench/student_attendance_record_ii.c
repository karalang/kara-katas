// Benchmark for #552: C mirror of the ★ arm (six counters, rolled); see
// student_attendance_record_ii.kara. The day's new counters are a local
// array of six, where Kāra makes a fresh Vec.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t check_record(int64_t n) {
    const int64_t m = 1000000007;
    int64_t count[6] = {1, 0, 0, 0, 0, 0};
    for (int64_t d = 0; d < n; d++) {
        int64_t next[6] = {0, 0, 0, 0, 0, 0};
        for (int a = 0; a < 2; a++)
            for (int l = 0; l < 3; l++) {
                int64_t c = count[a * 3 + l];
                if (c == 0) continue;
                next[a * 3] = (next[a * 3] + c) % m;
                if (a == 0) next[3] = (next[3] + c) % m;
                if (l < 2) next[a * 3 + l + 1] = (next[a * 3 + l + 1] + c) % m;
            }
        memcpy(count, next, sizeof count);
    }
    int64_t total = 0;
    for (int k = 0; k < 6; k++) total = (total + count[k]) % m;
    return total;
}

int main(void) {
    int64_t checksum = 0, days = 0;
    for (int64_t k = 0; k < 100; k++) {
        int64_t n = 100000 - (k * 997) % 1000;
        days += n;
        checksum = (checksum * 31 + check_record(n)) % 1000000007;
    }
    printf("100 lengths, %lld days: checksum %lld\n", (long long)days, (long long)checksum);
    return 0;
}
