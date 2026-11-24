// LeetCode #1342 bench in C: the ★ arm (halve an even number, take one
// from an odd one, count the steps) on the same 5 passes over 10^6 + 1
// numbers.
#include <stdint.h>
#include <stdio.h>

static int number_of_steps(int num) {
    int steps = 0;
    while (num > 0) {
        if (num % 2 == 0) num /= 2;
        else num -= 1;
        steps++;
    }
    return steps;
}

int main(void) {
    int64_t check = 0;
    for (int64_t pass = 0; pass < 5; pass++) {
        for (int64_t x = 0; x < 1000001; x++) {
            int steps = number_of_steps((int)((x + check) % 1000001));
            check = (check * 31 + steps + pass) % 1000000007;
        }
    }
    printf("5 passes over 10^6 + 1 numbers: checksum %lld\n", (long long)check);
    return 0;
}
