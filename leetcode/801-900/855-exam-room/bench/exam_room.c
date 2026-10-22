// Benchmark for #855: Exam Room -- the sorted-vector arm, mirroring
// exam_room.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t n;
    int64_t *taken;
    int64_t len, cap;
} ExamRoom;

static void room_init(ExamRoom *r, int64_t n) {
    r->n = n;
    r->len = 0;
    r->cap = 16;
    r->taken = malloc(r->cap * sizeof(int64_t));
}

static void insert_at(ExamRoom *r, int64_t at, int64_t v) {
    if (r->len == r->cap) {
        r->cap *= 2;
        r->taken = realloc(r->taken, r->cap * sizeof(int64_t));
    }
    memmove(r->taken + at + 1, r->taken + at, (r->len - at) * sizeof(int64_t));
    r->taken[at] = v;
    r->len++;
}

static int64_t seat(ExamRoom *r) {
    if (r->len == 0) {
        insert_at(r, 0, 0);
        return 0;
    }
    int64_t best = r->taken[0];
    int64_t best_seat = 0;
    for (int64_t i = 0; i + 1 < r->len; i++) {
        int64_t half = (r->taken[i + 1] - r->taken[i]) / 2;
        if (half > best) {
            best = half;
            best_seat = r->taken[i] + half;
        }
    }
    int64_t last = r->taken[r->len - 1];
    if (r->n - 1 - last > best) best_seat = r->n - 1;
    int64_t lo = 0, hi = r->len;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (r->taken[mid] < best_seat) lo = mid + 1;
        else hi = mid;
    }
    insert_at(r, lo, best_seat);
    return best_seat;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static void leave(ExamRoom *r, int64_t p) {
    int64_t *at = bsearch(&p, r->taken, r->len, sizeof(int64_t), cmp);
    int64_t i = at - r->taken;
    memmove(r->taken + i, r->taken + i + 1, (r->len - i - 1) * sizeof(int64_t));
    r->len--;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t rounds = 300, calls = 4000, n = 1000000000;
    int64_t seed = 855, total = 0, checksum = 0;
    int64_t *seated = malloc(calls * sizeof(int64_t));
    for (int64_t r = 0; r < rounds; r++) {
        ExamRoom room;
        room_init(&room, n);
        int64_t count = 0;
        for (int64_t c = 0; c < calls; c++) {
            if (count == 0 || next_random(&seed) % 3 != 0) {
                int64_t p = seat(&room);
                seated[count++] = p;
                total += p;
                checksum = (checksum * 31 + p % 1000003) % 1000000007;
            } else {
                int64_t i = next_random(&seed) % count;
                int64_t p = seated[i];
                seated[i] = seated[--count];
                leave(&room, p);
            }
        }
        free(room.taken);
    }
    free(seated);
    printf("%lld rooms of 4000 calls: seats sum to %lld, checksum %lld\n", (long long)rounds,
           (long long)total, (long long)checksum);
    return 0;
}
