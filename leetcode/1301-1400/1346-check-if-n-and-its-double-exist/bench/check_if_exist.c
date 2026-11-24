// LeetCode #1346 bench in C: the ★ arm (the values seen so far, each new
// value checked for its double and, when even, its half) on the same 2000
// arrays of 500 values and 100 passes. C has no set, so a value is marked
// seen in an array over the 4001 values a double can take, stamped with
// the call's number so it never needs clearing.
#include <stdint.h>
#include <stdio.h>

static int stamp[4001];
static int calls = 0;

static int check_if_exist(const int *arr, int n) {
    calls++;
    for (int i = 0; i < n; i++) {
        int x = arr[i];
        if (stamp[2 * x + 2000] == calls || (x % 2 == 0 && stamp[x / 2 + 2000] == calls)) return 1;
        stamp[x + 2000] = calls;
    }
    return 0;
}

static int64_t seed = 1346;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int arrays[2000][500];
    for (int a = 0; a < 2000; a++)
        for (int i = 0; i < 500; i++) arrays[a][i] = (int)(2 * (next_random() % 1000) - 999);
    int64_t check = 0;
    for (int64_t pass = 0; pass < 100; pass++) {
        for (int a = 0; a < 2000; a++) {
            arrays[a][check % 500] = (int)((check / 7) % 2001 - 1000);
            int yes = check_if_exist(arrays[a], 500);
            check = (check * 31 + (yes ? 2 : 1) + pass) % 1000000007;
        }
    }
    printf("100 passes over 2000 arrays of 500: checksum %lld\n", (long long)check);
    return 0;
}
