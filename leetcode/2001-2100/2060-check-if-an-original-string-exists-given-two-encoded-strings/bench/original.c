// LeetCode #2060: Check if an Original String Exists Given Two Encoded
// Strings -- C mirror of the ★ arm's benchmark (original.kara): the same
// 2000 pairs, each answered by one search over (place, place, lead) with a
// set of the states tried (open addressing, doubled when half full).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t i, j, lead; int used; } Slot;
static Slot *slots;
static size_t cap, count;

static uint64_t hash3(int64_t i, int64_t j, int64_t lead) {
    uint64_t h = (uint64_t)i * 0x9E3779B97F4A7C15ULL;
    h ^= (uint64_t)j + 0x632BE59BD9B4E019ULL + (h << 6) + (h >> 2);
    h ^= (uint64_t)lead + 0x9E3779B97F4A7C15ULL + (h << 6) + (h >> 2);
    h ^= h >> 31;
    h *= 0xBF58476D1CE4E5B9ULL;
    return h ^ (h >> 29);
}

static void put(Slot *t, size_t c, int64_t i, int64_t j, int64_t lead) {
    size_t p = hash3(i, j, lead) & (c - 1);
    while (t[p].used) p = (p + 1) & (c - 1);
    t[p].i = i; t[p].j = j; t[p].lead = lead; t[p].used = 1;
}

// Returns 1 when the state was new (and records it).
static int insert(int64_t i, int64_t j, int64_t lead) {
    size_t p = hash3(i, j, lead) & (cap - 1);
    while (slots[p].used) {
        if (slots[p].i == i && slots[p].j == j && slots[p].lead == lead) return 0;
        p = (p + 1) & (cap - 1);
    }
    if (2 * (count + 1) > cap) {
        size_t nc = cap * 2;
        Slot *nt = calloc(nc, sizeof(Slot));
        for (size_t q = 0; q < cap; q++)
            if (slots[q].used) put(nt, nc, slots[q].i, slots[q].j, slots[q].lead);
        free(slots);
        slots = nt;
        cap = nc;
    }
    put(slots, cap, i, j, lead);
    count++;
    return 1;
}

static const char *A, *B;
static int64_t NA, NB;

static int isdig(char c) { return c >= '0' && c <= '9'; }

static int search(int64_t i, int64_t j, int64_t lead) {
    if (i == NA && j == NB) return lead == 0;
    if (!insert(i, j, lead)) return 0;
    if (i < NA && isdig(A[i])) {
        int64_t num = 0, k = i;
        while (k < NA && isdig(A[k])) {
            num = num * 10 + (A[k] - '0');
            k++;
            if (search(k, j, lead + num)) return 1;
        }
        return 0;
    }
    if (j < NB && isdig(B[j])) {
        int64_t num = 0, k = j;
        while (k < NB && isdig(B[k])) {
            num = num * 10 + (B[k] - '0');
            k++;
            if (search(i, k, lead - num)) return 1;
        }
        return 0;
    }
    if (lead > 0) return j < NB && search(i, j + 1, lead - 1);
    if (lead < 0) return i < NA && search(i + 1, j, lead + 1);
    return i < NA && j < NB && A[i] == B[j] && search(i + 1, j + 1, 0);
}

static int possibly_equals(const char *s1, const char *s2) {
    A = s1; B = s2; NA = (int64_t)strlen(s1); NB = (int64_t)strlen(s2);
    cap = 64; count = 0;
    slots = calloc(cap, sizeof(Slot));
    int ok = search(0, 0, 0);
    free(slots);
    return ok;
}

static int64_t seed = 2060;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void dense(char *s) {
    size_t n = 0;
    s[0] = 0;
    for (;;) {
        char run[4];
        int64_t len = next_random() % 3 + 1;
        for (int64_t q = 0; q < len; q++) run[q] = (char)('1' + next_random() % 9);
        char letter = next_random() % 2 == 0 ? 'u' : 'v';
        if (n + (size_t)len + 1 > 40) return;
        memcpy(s + n, run, (size_t)len);
        n += (size_t)len;
        s[n++] = letter;
        s[n] = 0;
    }
}

int main(void) {
    char s1[48], s2[48];
    int possible = 0;
    int64_t check = 0;
    for (int t = 0; t < 2000; t++) {
        dense(s1);
        dense(s2);
        int ok = possibly_equals(s1, s2);
        if (ok) possible++;
        check = (check * 31 + (ok ? 2 : 1)) % 1000000007;
    }
    printf("2000 pairs: %d possible, checksum %lld\n", possible, (long long)check);
    return 0;
}
