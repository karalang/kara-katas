// LeetCode #2073: Time Needed to Buy Tickets -- C mirror of the ★ arm's
// benchmark (tickets.kara): 20000 lines of 100 people, every place in
// every line asked about, 2000000 answers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t time_required_to_buy(const int64_t *tickets, int64_t n, int64_t k) {
    int64_t want = tickets[k], time = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t cap = i <= k ? want : want - 1;
        time += tickets[i] < cap ? tickets[i] : cap;
    }
    return time;
}

static int64_t seed = 2073;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *lines = malloc(sizeof(int64_t) * 20000 * 100);
    for (int64_t l = 0; l < 20000; l++)
        for (int64_t j = 0; j < 100; j++) lines[l * 100 + j] = next_random() % 100 + 1;
    int64_t total = 0, check = 0;
    for (int64_t l = 0; l < 20000; l++)
        for (int64_t k = 0; k < 100; k++) {
            int64_t a = time_required_to_buy(lines + l * 100, 100, k);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    printf("2000000 answers: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(lines);
    return 0;
}
