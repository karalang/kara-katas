// LeetCode #1598: Crawler Log Folder
// -- the bench in C, mirroring crawler.kara: only the depth matters,
// read by comparing each log, on 2000 logs of 5000 operations, all drawn
// first; each log is its own malloc'd string, as Kāra's String is.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int32_t min_operations(char **logs, int n) {
    int32_t depth = 0;
    for (int i = 0; i < n; i++) {
        if (strcmp(logs[i], "../") == 0) {
            if (depth > 0) depth--;
        } else if (strcmp(logs[i], "./") != 0) {
            depth++;
        }
    }
    return depth;
}

int main(void) {
    enum { N = 2000, L = 5000 };
    int64_t seed = 1598;
    char ***all = malloc(sizeof(char **) * N);
    for (int g = 0; g < N; g++) {
        all[g] = malloc(sizeof(char *) * L);
        for (int i = 0; i < L; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int64_t r = seed / 65536 % 8;
            char buf[8];
            if (r < 2) strcpy(buf, "../");
            else if (r < 4) strcpy(buf, "./");
            else snprintf(buf, sizeof buf, "d%lld/", (long long)(r - 3));
            all[g][i] = strdup(buf);
        }
    }
    int64_t check = 0, total = 0;
    for (int g = 0; g < N; g++) {
        int32_t answer = min_operations(all[g], L);
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("2000 logs of 5000 operations: total %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int g = 0; g < N; g++) {
        for (int i = 0; i < L; i++) free(all[g][i]);
        free(all[g]);
    }
    free(all);
    return 0;
}
