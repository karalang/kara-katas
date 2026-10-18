// LeetCode 752 — Open the Lock, bench: the ★ arm (breadth-first over
// numbers) against 500 dead ends that keep changing. Mirrors open_lock.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t open_lock(char deadends[][5], int64_t count, const char *target) {
    static int blocked[10000];
    static int64_t dist[10000], queue[10000];
    for (int i = 0; i < 10000; i++) blocked[i] = 0;
    for (int64_t i = 0; i < count; i++) {
        int64_t v = 0;
        for (int k = 0; k < 4; k++) v = v * 10 + (deadends[i][k] - '0');
        blocked[v] = 1;
    }
    int64_t goal = 0;
    for (int k = 0; k < 4; k++) goal = goal * 10 + (target[k] - '0');
    if (blocked[0]) return -1;
    for (int i = 0; i < 10000; i++) dist[i] = -1;
    dist[0] = 0;
    int64_t head = 0, tail = 0;
    queue[tail++] = 0;
    while (head < tail) {
        int64_t at = queue[head++];
        if (at == goal) return dist[at];
        int64_t place = 1;
        for (int w = 0; w < 4; w++) {
            int64_t digit = at / place % 10;
            static const int64_t steps[2] = {1, 9};
            for (int s = 0; s < 2; s++) {
                int64_t next = at + ((digit + steps[s]) % 10 - digit) * place;
                if (!blocked[next] && dist[next] == -1) {
                    dist[next] = dist[at] + 1;
                    queue[tail++] = next;
                }
            }
            place *= 10;
        }
    }
    return -1;
}

static int64_t seed = 752;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void four(int64_t x, char *out) {
    snprintf(out, 5, "%lld%lld%lld%lld", (long long)(x / 1000), (long long)(x / 100 % 10),
             (long long)(x / 10 % 10), (long long)(x % 10));
}

int main(void) {
    const int64_t rounds = 3000;
    static char deadends[500][5];
    for (int i = 0; i < 500; i++) four(1 + next_random() % 9999, deadends[i]);
    int64_t total = 0, stuck = 0;
    char target[5];
    for (int64_t r = 0; r < rounds; r++) {
        for (int k = 0; k < 5; k++) {
            int64_t i = next_random() % 500;
            four(1 + next_random() % 9999, deadends[i]);
        }
        four(next_random() % 10000, target);
        int64_t turns = open_lock(deadends, 500, target);
        if (turns == -1) stuck++;
        else total += turns;
    }
    printf("%lld locks with 500 dead ends: %lld cannot open, the rest take %lld turns in all\n", (long long)rounds,
           (long long)stuck, (long long)total);
    return 0;
}
