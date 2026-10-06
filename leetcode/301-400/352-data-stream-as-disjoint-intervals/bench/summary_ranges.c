// Bench mirror of summary_ranges.kara (the sorted-vector arm), same algorithm.
// Growable arrays of starts and ends; insert and remove shift with memmove.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *starts, *ends;
    int64_t len, cap;
} SummaryRanges;

static void sr_init(SummaryRanges *sr) {
    sr->starts = NULL;
    sr->ends = NULL;
    sr->len = 0;
    sr->cap = 0;
}

static void sr_free(SummaryRanges *sr) {
    free(sr->starts);
    free(sr->ends);
}

static int64_t first_after(const SummaryRanges *sr, int64_t value) {
    int64_t lo = 0, hi = sr->len;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (sr->starts[mid] <= value) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static void insert_at(SummaryRanges *sr, int64_t i, int64_t value) {
    if (sr->len == sr->cap) {
        sr->cap = sr->cap ? sr->cap * 2 : 4;
        sr->starts = realloc(sr->starts, sr->cap * sizeof(int64_t));
        sr->ends = realloc(sr->ends, sr->cap * sizeof(int64_t));
    }
    memmove(sr->starts + i + 1, sr->starts + i, (sr->len - i) * sizeof(int64_t));
    memmove(sr->ends + i + 1, sr->ends + i, (sr->len - i) * sizeof(int64_t));
    sr->starts[i] = value;
    sr->ends[i] = value;
    sr->len++;
}

static void remove_at(SummaryRanges *sr, int64_t i) {
    memmove(sr->starts + i, sr->starts + i + 1, (sr->len - i - 1) * sizeof(int64_t));
    memmove(sr->ends + i, sr->ends + i + 1, (sr->len - i - 1) * sizeof(int64_t));
    sr->len--;
}

static void add_num(SummaryRanges *sr, int64_t value) {
    int64_t i = first_after(sr, value);
    int joins_left = i > 0 && sr->ends[i - 1] >= value - 1;
    if (i > 0 && sr->ends[i - 1] >= value) return;
    int joins_right = i < sr->len && sr->starts[i] == value + 1;
    if (joins_left && joins_right) {
        sr->ends[i - 1] = sr->ends[i];
        remove_at(sr, i);
    } else if (joins_left) {
        sr->ends[i - 1] = value;
    } else if (joins_right) {
        sr->starts[i] = value;
    } else {
        insert_at(sr, i, value);
    }
}

// get_intervals: copy the pairs out, as the other languages do.
static int64_t *get_intervals(const SummaryRanges *sr) {
    int64_t *out = malloc((sr->len ? sr->len : 1) * 2 * sizeof(int64_t));
    for (int64_t i = 0; i < sr->len; i++) {
        out[2 * i] = sr->starts[i];
        out[2 * i + 1] = sr->ends[i];
    }
    return out;
}

static int64_t next_value(int64_t *state, int64_t limit) {
    *state = (*state * 1103515245 + 12345) % 2147483648LL;
    return (*state >> 8) % (limit + 1);
}

int main(void) {
    int64_t rounds = 150, sink = 0;
    for (int64_t r = 0; r < rounds; r++) {
        SummaryRanges stream;
        sr_init(&stream);
        int64_t state = 352 + r;
        for (int64_t i = 1; i < 30001; i++) {
            add_num(&stream, next_value(&state, 10000));
            if (i % 3000 == 0) {
                int64_t n = stream.len;
                int64_t *iv = get_intervals(&stream);
                for (int64_t k = 0; k < n; k++)
                    sink = (sink * 31 + iv[2 * k] * 7 + iv[2 * k + 1] + r) % 1000000007;
                free(iv);
            }
        }
        sr_free(&stream);
    }
    printf("sink %lld\n", (long long)sink);
    return 0;
}
