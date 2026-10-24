// LeetCode #957: Prison Cells After N Days -- C mirror of the Kara bench
// program (a day per state seen). The first day of each row sits in an
// open-addressing table of 64 slots with linear probing.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void next_day(const long *cells, long *out) {
    memset(out, 0, sizeof(long) * 8);
    for (int i = 1; i < 7; i++) {
        if (cells[i - 1] == cells[i + 1]) {
            out[i] = 1;
        }
    }
}

static long code(const long *cells) {
    long c = 0;
    for (int i = 0; i < 8; i++) {
        c = c * 2 + cells[i];
    }
    return c;
}

typedef struct {
    long keys[64];
    long days[64];
    char used[64];
} Seen;

static long slot(const Seen *t, long key) {
    long i = (key * 37) & 63;
    while (t->used[i] && t->keys[i] != key) {
        i = (i + 1) & 63;
    }
    return i;
}

static void prison_after_n_days(const long *cells, long n, long *row) {
    Seen seen;
    memset(seen.used, 0, sizeof(seen.used));
    long next[8];
    memcpy(row, cells, sizeof(long) * 8);
    long day = 0, left = n;
    while (left > 0) {
        long i = slot(&seen, code(row));
        if (seen.used[i]) {
            left = left % (day - seen.days[i]);
            memset(seen.used, 0, sizeof(seen.used));
            if (left == 0) {
                break;
            }
            i = slot(&seen, code(row));
        }
        seen.used[i] = 1;
        seen.keys[i] = code(row);
        seen.days[i] = day;
        next_day(row, next);
        memcpy(row, next, sizeof(long) * 8);
        day++;
        left--;
    }
}

int main(void) {
    const long rounds = 2000;
    long rows[256][8];
    for (long b = 0; b < 256; b++) {
        for (int i = 0; i < 8; i++) {
            rows[b][i] = (b >> (7 - i)) & 1;
        }
    }
    long total = 0, check = 0;
    long out[8];
    for (long r = 0; r < rounds; r++) {
        for (long b = 0; b < 256; b++) {
            prison_after_n_days(rows[b], 1000000000 - r, out);
            long c = code(out);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    printf("%ld rounds over all 256 rows: rows adding to %ld, checksum %ld\n", rounds, total, check);
    return 0;
}
