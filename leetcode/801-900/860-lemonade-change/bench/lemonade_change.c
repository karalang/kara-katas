// LeetCode #860: Lemonade Change -- C mirror of the bench program (the ★
// arm, count the fives and tens, pay a twenty with a ten when there is one).
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool lemonade_change(const int64_t *bills, int64_t n) {
    int64_t fives = 0, tens = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t b = bills[i];
        if (b == 5) {
            fives++;
        } else if (b == 10) {
            if (fives == 0) return false;
            fives--;
            tens++;
        } else if (tens > 0 && fives > 0) {
            tens--;
            fives--;
        } else if (fives >= 3) {
            fives -= 3;
        } else {
            return false;
        }
    }
    return true;
}

static int64_t seed = 860;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t n = 100000;
    int64_t *bills = malloc(sizeof(int64_t) * n);
    int64_t fives = 0, tens = 0;
    for (int64_t k = 0; k < n; k++) {
        int64_t r = next_random() % 10;
        if (r >= 8 && tens > 0 && fives > 0) {
            bills[k] = 20; tens--; fives--;
        } else if (r >= 8 && fives >= 3) {
            bills[k] = 20; fives -= 3;
        } else if (r >= 5 && fives > 0) {
            bills[k] = 10; fives--; tens++;
        } else {
            bills[k] = 5; fives++;
        }
    }
    int64_t served = 0, check = 0;
    for (int64_t r = 0; r < 1000; r++) {
        int64_t i = next_random() % n;
        int64_t old = bills[i];
        bills[i] = old == 5 ? 10 : old == 10 ? 20 : 5;
        bool yes = lemonade_change(bills, n);
        bills[i] = old;
        if (yes) served++;
        check = (check * 31 + (yes ? r + 2 : 1)) % 1000000007;
    }
    printf("1000 rounds on 100000 bills: %lld served, checksum %lld\n", (long long)served, (long long)check);
    free(bills);
    return 0;
}
