// LeetCode #1024: Video Stitching -- bench
// Mirrors ./video_stitching.kara; see ../README.md § Benchmarks.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t video_stitching(const int64_t (*clips)[2], int n, int64_t time) {
    int64_t *furthest = calloc((size_t)(time + 1), sizeof(int64_t));
    for (int i = 0; i < n; i++) {
        if (clips[i][0] <= time && clips[i][1] > furthest[clips[i][0]]) {
            furthest[clips[i][0]] = clips[i][1];
        }
    }
    int64_t taken = 0, covered = 0, reach = 0;
    for (int64_t t = 0; t < time; t++) {
        if (furthest[t] > reach) reach = furthest[t];
        if (reach <= t) {
            free(furthest);
            return -1;
        }
        if (t == covered) {
            taken++;
            covered = reach;
        }
    }
    free(furthest);
    return taken;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

typedef struct {
    int64_t (*clips)[2];
    int n;
    int64_t time;
} Case;

int main(void) {
    const int count = 2000;
    const int rounds = 500;
    int64_t seed = 1024;
    Case *cases = malloc(sizeof(Case) * count);
    int64_t total_clips = 0;
    for (int c = 0; c < count; c++) {
        int64_t time = 50 + next_random(&seed) % 51;
        int64_t (*clips)[2] = malloc(sizeof(int64_t[2]) * 101);
        int n = 0;
        int64_t at = 0;
        while (at < time) {
            int64_t length = 1 + next_random(&seed) % 10;
            int64_t back = next_random(&seed) % 3;
            clips[n][0] = at - back > 0 ? at - back : 0;
            clips[n][1] = at + length < 100 ? at + length : 100;
            n++;
            at += length;
        }
        int64_t extra = next_random(&seed) % (101 - n);
        for (int64_t k = 0; k < extra; k++) {
            int64_t start = next_random(&seed) % (time + 1);
            int64_t end = start + next_random(&seed) % 21;
            if (end > 100) end = 100;
            int64_t place = next_random(&seed) % (n + 1);
            memmove(clips[place + 1], clips[place], sizeof(int64_t[2]) * (size_t)(n - place));
            clips[place][0] = start;
            clips[place][1] = end;
            n++;
        }
        total_clips += n;
        cases[c].clips = clips;
        cases[c].n = n;
        cases[c].time = time;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            int64_t answer = video_stitching((const int64_t (*)[2])cases[c].clips, cases[c].n, cases[c].time);
            sum += answer;
            check = (check * 131 + answer + 1) % 1000000007;
        }
    }
    printf("%d cases, %lld clips, %d rounds: sum %lld, checksum %lld\n", count, (long long)total_clips, rounds,
           (long long)sum, (long long)check);
    return 0;
}
