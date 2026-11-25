// LeetCode #1348 bench -- C: each name's times in the order recorded, the
// names in a small table searched by strcmp; a query walks every time of
// its name into per-chunk counts.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[16];
    int *times;
    long len, cap;
} Series;

static Series series[64];
static int nseries;

static Series *find(const char *name, int create) {
    for (int i = 0; i < nseries; i++)
        if (strcmp(series[i].name, name) == 0) return &series[i];
    if (!create) return NULL;
    Series *s = &series[nseries++];
    strcpy(s->name, name);
    s->times = NULL;
    s->len = s->cap = 0;
    return s;
}

static void record_tweet(const char *name, int time) {
    Series *s = find(name, 1);
    if (s->len == s->cap) {
        s->cap = s->cap ? 2 * s->cap : 8;
        s->times = realloc(s->times, s->cap * sizeof(int));
    }
    s->times[s->len++] = time;
}

static int size_of(const char *freq) {
    if (strcmp(freq, "minute") == 0) return 60;
    if (strcmp(freq, "hour") == 0) return 3600;
    return 86400;
}

// fills counts, returns how many chunks
static int get_counts(const char *freq, const char *name, int start, int end, int *counts) {
    int size = size_of(freq);
    int chunks = (end - start) / size + 1;
    memset(counts, 0, chunks * sizeof(int));
    Series *s = find(name, 0);
    if (s)
        for (long i = 0; i < s->len; i++) {
            int t = s->times[i];
            if (t >= start && t <= end) counts[(t - start) / size]++;
        }
    return chunks;
}

int main(void) {
    const char *names[10] = {"n0", "n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9"};
    const char *freqs[3] = {"minute", "hour", "day"};
    long long seed = 1348;
    for (int i = 0; i < 100000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        const char *name = names[(seed / 65536) % 10];
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        record_tweet(name, (int)((seed / 65536) % 1000001));
    }
    static int counts[10001];
    long long check = 0;
    for (long long r = 0; r < 10000; r++) {
        record_tweet(names[check % 10], (int)(check % 1000001));
        long long start = (check / 11) % 990001;
        int chunks = get_counts(freqs[(check / 13) % 3], names[(check / 17) % 10], (int)start, (int)(start + 10000), counts);
        for (int k = 0; k < chunks; k++) check = (check * 31 + counts[k]) % 1000000007;
        check = (check * 31 + r) % 1000000007;
    }
    printf("10000 rounds over 100000 tweets: checksum %lld\n", check);
    return 0;
}
