// LeetCode #1345 bench in C: the ★ arm (a breadth-first search over i - 1,
// i + 1 and the indices of the same value, each value's list used once)
// on the same 10 arrays of 5 * 10^4 values and 30 passes. C has no map, so
// each value gets a group number from an open-addressing table, the
// groups' indices are laid out one after another, and a used group is
// marked rather than removed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS (1 << 17)

static int min_jumps(const int *arr, int n) {
    static int keys[SLOTS], ids[SLOTS];
    static char used_slot[SLOTS];
    int *group = malloc(sizeof(int) * (size_t)n);
    int *count = calloc((size_t)n + 1, sizeof(int));
    memset(used_slot, 0, sizeof used_slot);
    int groups = 0;
    for (int i = 0; i < n; i++) {
        uint32_t h = ((uint32_t)arr[i] * 2654435761u) & (SLOTS - 1);
        while (used_slot[h] && keys[h] != arr[i]) h = (h + 1) & (SLOTS - 1);
        if (!used_slot[h]) {
            used_slot[h] = 1;
            keys[h] = arr[i];
            ids[h] = groups++;
        }
        group[i] = ids[h];
        count[ids[h] + 1]++;
    }
    for (int g = 0; g < groups; g++) count[g + 1] += count[g];
    int *start = malloc(sizeof(int) * ((size_t)groups + 1));
    memcpy(start, count, sizeof(int) * ((size_t)groups + 1));
    int *members = malloc(sizeof(int) * (size_t)n);
    for (int i = 0; i < n; i++) members[count[group[i]]++] = i;
    char *spent = calloc((size_t)groups, 1);
    int *steps = malloc(sizeof(int) * (size_t)n);
    for (int i = 0; i < n; i++) steps[i] = -1;
    int *queue = malloc(sizeof(int) * (size_t)n);
    int head = 0, tail = 0, answer = -1;
    steps[0] = 0;
    queue[tail++] = 0;
    while (head < tail) {
        int i = queue[head++];
        if (i == n - 1) {
            answer = steps[i];
            break;
        }
        int g = group[i];
        if (!spent[g]) {
            spent[g] = 1;
            for (int k = start[g]; k < start[g + 1]; k++) {
                int j = members[k];
                if (steps[j] < 0) {
                    steps[j] = steps[i] + 1;
                    queue[tail++] = j;
                }
            }
        }
        int around[2] = {i - 1, i + 1};
        for (int k = 0; k < 2; k++) {
            int j = around[k];
            if (j >= 0 && j < n && steps[j] < 0) {
                steps[j] = steps[i] + 1;
                queue[tail++] = j;
            }
        }
    }
    if (answer < 0) answer = steps[n - 1];
    free(group); free(count); free(start); free(members); free(spent); free(steps); free(queue);
    return answer;
}

static int64_t seed = 1345;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { N = 50000 };
    static int arrays[10][N];
    for (int a = 0; a < 10; a++)
        for (int i = 0; i < N; i++)
            arrays[a][i] = a % 2 == 0 ? (int)(1 + next_random() % 1000) : i / 2;
    int64_t check = 0;
    for (int64_t pass = 0; pass < 30; pass++) {
        for (int a = 0; a < 10; a++) {
            arrays[a][check % N] = (int)((check / 7) % 25000);
            int answer = min_jumps(arrays[a], N);
            check = (check * 31 + answer + pass) % 1000000007;
        }
    }
    printf("30 passes over 10 arrays of 5 * 10^4: checksum %lld\n", (long long)check);
    return 0;
}
