// Benchmark: LeetCode #1088 Confusing Number II -- mirrors
// confusing_number_ii.kara: a depth-first walk over the numbers made of the
// digits that rotate, each carrying its rotation, for 400 random n up to
// 10^9 drawn once.
#include <stdint.h>
#include <stdio.h>

static const int64_t DIGITS[5] = {0, 1, 6, 8, 9};

static int64_t rotated(int64_t d) {
    switch (d) {
    case 0: return 0;
    case 1: return 1;
    case 6: return 9;
    case 8: return 8;
    case 9: return 6;
    default: return -1;
    }
}

static int64_t count_from(int64_t num, int64_t rot, int64_t unit, int64_t n) {
    int64_t total = 0;
    for (int i = 0; i < 5; i++) {
        int64_t d = DIGITS[i];
        int64_t next = num * 10 + d;
        if (next > n) {
            break;
        }
        if (next == 0) {
            continue;
        }
        int64_t r = rotated(d) * unit + rot;
        if (next != r) {
            total += 1;
        }
        total += count_from(next, r, unit * 10, n);
    }
    return total;
}

static int64_t confusing_number_ii(int64_t n) { return count_from(0, 0, 1, n); }

static int64_t seed = 1088;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t ns[400];
    for (int i = 0; i < 400; i++) {
        int64_t a = next_random();
        int64_t hi = a * 32768 + next_random();
        ns[i] = hi % 1000000000 + 1;
    }
    int64_t total = 0, check = 0;
    for (int i = 0; i < 400; i++) {
        int64_t a = confusing_number_ii(ns[i]);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    printf("400 n up to 10^9: %lld confusing numbers, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
