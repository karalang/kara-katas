// LeetCode #1125: Smallest Sufficient Team -- the bench in C: the ★ arm,
// each skill found by name among the required ones, and the team for each
// mask a row of a fixed table with its length, -1 until reached. The same
// 8 problems and 8 rounds.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define SKILLS 16
#define PEOPLE 60

static char req[SKILLS][8];
static char people[8][PEOPLE][SKILLS][8];
static int counts[8][PEOPLE];
static int64_t team[1 << SKILLS][SKILLS];
static int len[1 << SKILLS];

static int bit_of(const char *s, int m) {
    for (int i = 0; i < m; i++)
        if (strcmp(req[i], s) == 0) return i;
    return -1;
}

static int smallest_sufficient_team(int m, char (*ps)[SKILLS][8], const int *cnt, int n, int64_t *out) {
    int full = (1 << m) - 1;
    for (int k = 0; k <= full; k++) len[k] = -1;
    len[0] = 0;
    for (int p = 0; p < n; p++) {
        int mask = 0;
        for (int j = 0; j < cnt[p]; j++) mask |= 1 << bit_of(ps[p][j], m);
        if (mask == 0) continue;
        for (int k = 0; k <= full; k++) {
            int grown = k | mask;
            if (grown == k || len[k] < 0) continue;
            if (len[grown] < 0 || len[k] + 1 < len[grown]) {
                memcpy(team[grown], team[k], sizeof(int64_t) * len[k]);
                team[grown][len[k]] = p;
                len[grown] = len[k] + 1;
            }
        }
    }
    memcpy(out, team[full], sizeof(int64_t) * len[full]);
    return len[full];
}

static int64_t seed = 1125;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int has(int j, int p, const char *s) {
    for (int k = 0; k < counts[j][p]; k++)
        if (strcmp(people[j][p][k], s) == 0) return k;
    return -1;
}

int main(void) {
    for (int i = 0; i < SKILLS; i++) snprintf(req[i], 8, "s%d", i);
    for (int j = 0; j < 8; j++)
        for (int p = 0; p < PEOPLE; p++)
            for (int i = 0; i < SKILLS; i++)
                if (next_random() % 100 < 20) strcpy(people[j][p][counts[j][p]++], req[i]);
    int64_t total = 0, check = 0, out[SKILLS];
    for (int64_t round = 0; round < 8; round++) {
        for (int j = 0; j < 8; j++) {
            int who = (int)(next_random() % 60);
            char skill[8];
            snprintf(skill, 8, "s%d", (int)(next_random() % 16));
            int at = has(j, who, skill);
            if (at >= 0) {
                for (int k = at; k + 1 < counts[j][who]; k++) strcpy(people[j][who][k], people[j][who][k + 1]);
                counts[j][who]--;
            } else {
                strcpy(people[j][who][counts[j][who]++], skill);
            }
            for (int i = 0; i < SKILLS; i++) {
                int found = 0;
                for (int p = 0; p < PEOPLE && !found; p++) found = has(j, p, req[i]) >= 0;
                if (!found) {
                    int next = (who + 1) % 60;
                    strcpy(people[j][next][counts[j][next]++], req[i]);
                }
            }
            int size = smallest_sufficient_team(SKILLS, people[j], counts[j], PEOPLE, out);
            total += size;
            for (int k = 0; k < size; k++) check = (check * 61 + out[k] + 1) % 1000000007;
            check = (check * 17 + round) % 1000000007;
        }
    }
    printf("8 rounds over 8 problems of 16 skills and 60 people: team sizes total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
