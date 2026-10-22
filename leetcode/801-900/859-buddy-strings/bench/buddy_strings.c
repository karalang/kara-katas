// LeetCode #859: Buddy Strings -- C mirror of the bench program (the ★ arm,
// one pass over the positions where the strings differ).
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool buddy_strings(const uint8_t *a, int64_t na, const uint8_t *b, int64_t nb) {
    if (na != nb) return false;
    int64_t first = -1, second = -1;
    for (int64_t i = 0; i < na; i++) {
        if (a[i] != b[i]) {
            if (first < 0) first = i;
            else if (second < 0) second = i;
            else return false;
        }
    }
    if (first < 0) {
        bool seen[26] = {false};
        for (int64_t i = 0; i < na; i++) {
            int k = a[i] - 97;
            if (seen[k]) return true;
            seen[k] = true;
        }
        return false;
    }
    return second >= 0 && a[first] == b[second] && a[second] == b[first];
}

static int64_t seed = 859;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void swap(uint8_t *v, int64_t i, int64_t j) {
    uint8_t t = v[i];
    v[i] = v[j];
    v[j] = t;
}

int main(void) {
    const int64_t n = 20000;
    uint8_t *s = malloc(n), *goal = malloc(n);
    for (int64_t i = 0; i < n; i++) s[i] = (uint8_t)(97 + next_random() % 26);
    memcpy(goal, s, n);
    int64_t buddies = 0, check = 0;
    for (int64_t r = 0; r < 40000; r++) {
        int64_t i = next_random() % n;
        int64_t j = next_random() % n;
        int64_t kind = r % 3;
        uint8_t old = goal[i];
        if (kind == 1) goal[i] = (uint8_t)(97 + ((int64_t)old - 97 + 1 + next_random() % 25) % 26);
        else swap(goal, i, j);
        int64_t k = next_random() % n;
        int64_t l = next_random() % n;
        if (kind == 2) swap(goal, k, l);
        bool yes = buddy_strings(s, n, goal, n);
        if (kind == 2) swap(goal, k, l);
        if (kind == 1) goal[i] = old;
        else swap(goal, i, j);
        if (yes) buddies++;
        check = (check * 31 + (yes ? r + 2 : 1)) % 1000000007;
    }
    printf("40000 rounds on 20000 letters: %lld buddies, checksum %lld\n", (long long)buddies, (long long)check);
    free(s);
    free(goal);
    return 0;
}
