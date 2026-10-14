// LeetCode #635: Design Log Storage System -- benchmark, C.
//
// The ★ arm: timestamps compared as text after cutting them, and the
// bounds, to the granularity's length.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t id;
    char timestamp[20];
} Log;

typedef struct {
    Log *logs;
    int64_t len, cap;
} LogSystem;

typedef struct {
    int64_t *ids;
    int64_t len, cap;
} Ids;

static void put(LogSystem *s, int64_t id, const char *timestamp) {
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 16;
        s->logs = realloc(s->logs, s->cap * sizeof(Log));
    }
    s->logs[s->len].id = id;
    memcpy(s->logs[s->len].timestamp, timestamp, 20);
    s->len++;
}

static int64_t length(const char *granularity) {
    if (strcmp(granularity, "Year") == 0) return 4;
    if (strcmp(granularity, "Month") == 0) return 7;
    if (strcmp(granularity, "Day") == 0) return 10;
    if (strcmp(granularity, "Hour") == 0) return 13;
    if (strcmp(granularity, "Minute") == 0) return 16;
    return 19;
}

static Ids retrieve(const LogSystem *s, const char *start, const char *end, const char *granularity) {
    int64_t n = length(granularity);
    Ids out = {0};
    for (int64_t i = 0; i < s->len; i++) {
        const char *cut = s->logs[i].timestamp;
        if (memcmp(cut, start, n) >= 0 && memcmp(cut, end, n) <= 0) {
            if (out.len == out.cap) {
                out.cap = out.cap ? out.cap * 2 : 16;
                out.ids = realloc(out.ids, out.cap * sizeof(int64_t));
            }
            out.ids[out.len++] = s->logs[i].id;
        }
    }
    return out;
}

static int64_t seed = 635;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void random_time(char *out) {
    int64_t year = 2000 + next_random() % 18;
    int64_t month = 1 + next_random() % 12;
    int64_t day = 1 + next_random() % 31;
    int64_t hour = next_random() % 24;
    int64_t minute = next_random() % 60;
    int64_t second = next_random() % 60;
    snprintf(out, 20, "%04lld:%02lld:%02lld:%02lld:%02lld:%02lld", (long long)year,
             (long long)month, (long long)day, (long long)hour, (long long)minute,
             (long long)second);
}

int main(void) {
    const char *names[6] = {"Year", "Month", "Day", "Hour", "Minute", "Second"};
    LogSystem logs = {0};
    char t[20];
    for (int64_t id = 1; id <= 20000; id++) {
        random_time(t);
        put(&logs, id, t);
    }
    int64_t found = 0, checksum = 0;
    char start[20], end[20];
    for (int r = 0; r < 2000; r++) {
        random_time(start);
        random_time(end);
        const char *granularity = names[next_random() % 6];
        Ids ids = retrieve(&logs, start, end, granularity);
        for (int64_t i = 0; i < ids.len; i++) {
            found++;
            checksum = (checksum * 31 + ids.ids[i]) % 1000000007;
        }
        free(ids.ids);
    }
    printf("20000 logs, 2000 retrieves: %lld ids, checksum %lld\n", (long long)found,
           (long long)checksum);
    free(logs.logs);
    return 0;
}
