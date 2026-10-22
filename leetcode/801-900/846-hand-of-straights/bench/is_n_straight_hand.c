// Benchmark for #846: Hand of Straights -- C twin of the Kāra open-groups
// arm (sorted runs and a queue of open groups).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define N 10000

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t cards[N];
static int64_t started[N];

static int is_n_straight_hand(const int64_t *hand, int64_t n, int64_t group_size) {
    if (n % group_size != 0) return 0;
    memcpy(cards, hand, sizeof(int64_t) * n);
    qsort(cards, n, sizeof(int64_t), cmp_i64);
    // `started` is a ring buffer of at most group_size entries
    int64_t head = 0, len = 0;
    int64_t open = 0, last = 0, i = 0;
    while (i < n) {
        int64_t value = cards[i], count = 0;
        while (i < n && cards[i] == value) {
            count++;
            i++;
        }
        if (open > 0 && (value != last + 1 || count < open)) return 0;
        started[(head + len) % group_size] = count - open;
        len++;
        last = value;
        open = count;
        if (len == group_size) {
            open -= started[head];
            head = (head + 1) % group_size;
            len--;
        }
    }
    return open == 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 3000;
    const int64_t sizes[8] = {1, 2, 4, 5, 10, 16, 100, 1000};
    int64_t seed = 846;
    static int64_t hands[64][N];
    int64_t group_sizes[64];
    for (int64_t g = 0; g < count; g++) {
        int64_t group_size = sizes[g % 8];
        int64_t window = 1 + next_random(&seed) % 20000;
        int64_t *hand = hands[g];
        int64_t len = 0;
        while (len < N) {
            int64_t start = 999000000 + next_random(&seed) % window;
            for (int64_t j = 0; j < group_size; j++) hand[len++] = start + j;
        }
        for (int64_t i = 0; i < N; i++) {
            int64_t j = i + next_random(&seed) % (N - i);
            int64_t t = hand[i];
            hand[i] = hand[j];
            hand[j] = t;
        }
        if (g % 4 == 3) {
            int64_t at = next_random(&seed) % N;
            hand[at] += 1;
        }
        group_sizes[g] = group_size;
    }
    int64_t splits = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int ok = is_n_straight_hand(hands[round % count], N, group_sizes[round % count]);
        if (ok) splits++;
        checksum = (checksum * 31 + round % count + (ok ? 1 : 0)) % 1000000007;
    }
    printf("%lld rounds of %lld hands: %lld split, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)splits, (long long)checksum);
    return 0;
}
