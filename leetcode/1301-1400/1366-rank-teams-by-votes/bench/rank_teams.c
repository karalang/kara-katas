// LeetCode #1366 bench -- C: how many votes put each team in each place
// counted, and the teams sorted by those counts, then by letter.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ELECTIONS 20
#define VOTES 1000
#define TEAMS 26

static int64_t counts[26][TEAMS];
static size_t places;

static int by_counts(const void *pa, const void *pb) {
    int a = *(const char *)pa - 'A', b = *(const char *)pb - 'A';
    for (size_t p = 0; p < places; p++) {
        if (counts[a][p] != counts[b][p]) return counts[a][p] > counts[b][p] ? -1 : 1;
    }
    return a - b;
}

static void rank_teams(char votes[][TEAMS + 1], size_t n, char *out) {
    places = strlen(votes[0]);
    memset(counts, 0, sizeof counts);
    for (size_t v = 0; v < n; v++) {
        for (size_t place = 0; place < places; place++) counts[votes[v][place] - 'A'][place] += 1;
    }
    memcpy(out, votes[0], places + 1);
    qsort(out, places, 1, by_counts);
}

static int64_t seed = 1366;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char elections[ELECTIONS][VOTES][TEAMS + 1];

int main(void) {
    // 20 elections of 1000 votes over all 26 teams, the constraints' most,
    // built once; then 3000 rounds, each swapping two places of one vote,
    // all drawn from the checksum so far, ranking that election and
    // folding the ranking into the checksum
    for (int e = 0; e < ELECTIONS; e++) {
        for (int v = 0; v < VOTES; v++) {
            char *vote = elections[e][v];
            memcpy(vote, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", TEAMS + 1);
            for (int64_t i = 1; i < TEAMS; i++) {
                int64_t j = next_random() % (i + 1);
                char held = vote[i];
                vote[i] = vote[j];
                vote[j] = held;
            }
        }
    }
    int64_t check = 0;
    char ranked[TEAMS + 1];
    for (int64_t r = 0; r < 3000; r++) {
        int64_t e = check % 20, v = (check / 20) % 1000;
        int64_t i = (check / 20000) % 26, j = (check / 520000) % 26;
        char *vote = elections[e][v];
        char held = vote[i];
        vote[i] = vote[j];
        vote[j] = held;
        rank_teams(elections[e], VOTES, ranked);
        for (size_t k = 0; ranked[k]; k++) check = (check * 31 + (unsigned char)ranked[k]) % 1000000007;
        check = (check + r) % 1000000007;
    }
    printf("3000 rounds over 20 elections of 1000 votes: checksum %lld\n", (long long)check);
    return 0;
}
