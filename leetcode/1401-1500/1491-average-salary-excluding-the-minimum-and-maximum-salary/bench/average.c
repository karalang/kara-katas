// LeetCode #1491: Average Salary Excluding the Minimum and Maximum Salary --
// the bench in C, mirroring average.kara: one pass keeping the sum, the
// least and the most.
#include <stdint.h>
#include <stdio.h>

static double average(const int32_t *salary, int n) {
    int32_t least = salary[0], most = salary[0];
    int64_t sum = 0;
    for (int i = 0; i < n; i++) {
        if (salary[i] < least) least = salary[i];
        if (salary[i] > most) most = salary[i];
        sum += salary[i];
    }
    return (double)(sum - least - most) / (double)(n - 2);
}

int main(void) {
    int32_t salary[100];
    for (int64_t k = 0; k < 100; k++) salary[k] = (int32_t)(1000 + 9000 * k);
    int64_t check = 0;
    for (int64_t pass = 0; pass < 2000000; pass++) {
        int64_t k = pass % 100;
        salary[k] = (int32_t)(1000 + 9000 * k + (check + pass) % 9000);
        // half away from zero, as Kāra's `round` is; the value is positive
        int64_t cents = (int64_t)(average(salary, 100) * 100.0 + 0.5);
        check = (check * 31 + cents) % 1000000007;
    }
    printf("2000000 calls: checksum %lld\n", (long long)check);
    return 0;
}
