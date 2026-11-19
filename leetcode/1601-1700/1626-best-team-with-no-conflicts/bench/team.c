// LeetCode #1626: Best Team With No Conflicts -- the bench in C,
// mirroring team.kara: sorted by (age, score), the best team ending at
// each player from every earlier player scoring no higher.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int32_t age, score;
} Player;

static int by_age_then_score(const void *x, const void *y) {
    const Player *a = x, *b = y;
    if (a->age != b->age) return a->age < b->age ? -1 : 1;
    return (a->score > b->score) - (a->score < b->score);
}

static int32_t best_team_score(const int32_t *scores, const int32_t *ages, int n) {
    Player *players = malloc(sizeof(Player) * (size_t)n);
    for (int i = 0; i < n; i++) players[i] = (Player){ages[i], scores[i]};
    qsort(players, (size_t)n, sizeof(Player), by_age_then_score);
    int64_t *best = malloc(sizeof(int64_t) * (size_t)n);
    int64_t answer = 0;
    for (int i = 0; i < n; i++) {
        int64_t score = players[i].score;
        best[i] = score;
        for (int j = 0; j < i; j++) {
            if (players[j].score <= score && best[j] + score > best[i]) best[i] = best[j] + score;
        }
        if (best[i] > answer) answer = best[i];
    }
    free(players);
    free(best);
    return (int32_t)answer;
}

static int64_t seed = 1626;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { TEAMS = 100, N = 1000 };
    static int32_t scores[TEAMS][N], ages[TEAMS][N];
    for (int t = 0; t < TEAMS; t++) {
        for (int i = 0; i < N; i++) {
            int64_t high = next_random();
            scores[t][i] = (int32_t)((high * 32768 + next_random()) % 1000000 + 1);
            ages[t][i] = (int32_t)(next_random() % 1000 + 1);
        }
    }
    int64_t check = 0, total = 0;
    for (int t = 0; t < TEAMS; t++) {
        int64_t got = best_team_score(scores[t], ages[t], N);
        total += got;
        check = (check * 31 + got + 1) % 1000000007;
    }
    printf("100 teams of 1000 players: best scores sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
