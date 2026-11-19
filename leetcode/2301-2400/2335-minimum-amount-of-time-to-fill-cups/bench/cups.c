// LeetCode #2335: Minimum Amount of Time to Fill Cups -- the bench, the ★
// arm in C: the larger of the most cups of one kind and half of all the
// cups, rounded up.
#include <stdint.h>
#include <stdio.h>

static int64_t fill_cups(const int64_t *amount) {
    int64_t most = amount[0];
    if (amount[1] > most) most = amount[1];
    if (amount[2] > most) most = amount[2];
    int64_t half = (amount[0] + amount[1] + amount[2] + 1) / 2;
    return most > half ? most : half;
}

int main(void) {
    int64_t amount[3] = {0, 0, 0};
    int64_t check = 0;
    for (int64_t p = 0; p < 3; p++)
        for (int64_t a = 0; a <= 100; a++)
            for (int64_t b = 0; b <= 100; b++)
                for (int64_t c = 0; c <= 100; c++) {
                    amount[0] = a;
                    amount[1] = b;
                    amount[2] = c;
                    check = (check * 31 + fill_cups(amount) + p) % 1000000007;
                }
    printf("3 passes over 101^3 amounts: checksum %lld\n", (long long)check);
    return 0;
}
