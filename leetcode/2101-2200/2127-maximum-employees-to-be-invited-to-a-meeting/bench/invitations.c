// LeetCode #2127: Maximum Employees to Be Invited to a Meeting -- the
// benchmark, the same algorithm as invitations.kara; the queue is an
// array with a head and a tail.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000

static int64_t seed = 2127;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t big(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

static int64_t indegree[N], chain[N], queue[N];

static int64_t maximum_invitations(const int64_t *favorite) {
    memset(indegree, 0, sizeof indegree);
    memset(chain, 0, sizeof chain);
    for (int i = 0; i < N; i++) indegree[favorite[i]]++;
    int head = 0, tail = 0;
    for (int i = 0; i < N; i++)
        if (indegree[i] == 0) queue[tail++] = i;
    while (head < tail) {
        int64_t i = queue[head++];
        int64_t f = favorite[i];
        if (chain[i] + 1 > chain[f]) chain[f] = chain[i] + 1;
        if (--indegree[f] == 0) queue[tail++] = f;
    }
    int64_t largest_cycle = 0, pairs = 0;
    for (int64_t i = 0; i < N; i++) {
        if (indegree[i] == 0) continue;
        int64_t length = 0, j = i;
        while (indegree[j] != 0) {
            indegree[j] = 0;
            length++;
            j = favorite[j];
        }
        if (length == 2)
            pairs += 2 + chain[i] + chain[favorite[i]];
        else if (length > largest_cycle)
            largest_cycle = length;
    }
    return largest_cycle > pairs ? largest_cycle : pairs;
}

int main(void) {
    int64_t *tables = malloc(sizeof(int64_t) * 20 * N);
    for (int t = 0; t < 20; t++)
        for (int64_t i = 0; i < N; i++)
            tables[t * N + i] = i < N / 4 ? (i ^ 1) : (i + 1 + big() % (N - 1)) % N;
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 10; round++) {
        for (int t = 0; t < 20; t++) {
            int64_t i = N / 4 + big() % (N - N / 4);
            tables[t * N + i] = (i + 1 + big() % (N - 1)) % N;
            int64_t invited = maximum_invitations(tables + t * N);
            total += invited;
            check = (check * 31 + invited + round) % 1000000007;
        }
    }
    printf("200 solves: %lld invited, checksum %lld\n", (long long)total, (long long)check);
    free(tables);
    return 0;
}
