// LeetCode #1845: Seat Reservation Manager -- the bench in C: the ★ arm,
// every unreserved seat in a binary heap that pops the smallest first,
// written out as C has none, over 50 runs of 10^5 calls on 50000 to 99999
// seats, each run's size and its place in one list of 10^6 draws, built
// once, taken from the checksum so far. A draw reserves a seat two times in
// three, and otherwise gives back a held seat it picks; every seat reserved
// goes into the checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *heap;
    int64_t size;
} SeatManager;

static void sift_down(int64_t *h, int64_t size, int64_t k) {
    for (;;) {
        int64_t small = k, l = 2 * k + 1, r = 2 * k + 2;
        if (l < size && h[l] < h[small]) small = l;
        if (r < size && h[r] < h[small]) small = r;
        if (small == k) return;
        int64_t t = h[k]; h[k] = h[small]; h[small] = t;
        k = small;
    }
}

static SeatManager seat_manager_new(int64_t n) {
    SeatManager m = { malloc(n * sizeof(int64_t)), n };
    for (int64_t i = 0; i < n; i++) m.heap[i] = i + 1;
    for (int64_t i = n / 2 - 1; i >= 0; i--) sift_down(m.heap, n, i);
    return m;
}

static int64_t reserve(SeatManager *m) {
    int64_t top = m->heap[0];
    m->heap[0] = m->heap[--m->size];
    sift_down(m->heap, m->size, 0);
    return top;
}

static void unreserve(SeatManager *m, int64_t seat_number) {
    int64_t k = m->size++;
    m->heap[k] = seat_number;
    while (k > 0 && m->heap[k] < m->heap[(k - 1) / 2]) {
        int64_t p = (k - 1) / 2, t = m->heap[k];
        m->heap[k] = m->heap[p]; m->heap[p] = t;
        k = p;
    }
}

int main(void) {
    int64_t seed = 1845;
    int64_t *draws = malloc(1000000 * sizeof *draws);
    for (int64_t i = 0; i < 1000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        draws[i] = seed / 65536;
    }
    int64_t check = 0;
    int64_t *held = malloc(100000 * sizeof *held);
    for (int run = 0; run < 50; run++) {
        int64_t n = 50000 + check % 50000;
        int64_t start = check % 500000;
        SeatManager seats = seat_manager_new(n);
        int64_t count = 0;
        for (int64_t k = 0; k < 100000; k++) {
            int64_t d = draws[start + k];
            if (count == 0 || (d % 3 != 0 && count < n)) {
                int64_t seat = reserve(&seats);
                check = (check * 31 + seat) % 1000000007;
                held[count++] = seat;
            } else {
                int64_t i = d % count;
                int64_t seat = held[i];
                held[i] = held[--count];
                unreserve(&seats, seat);
            }
        }
        free(seats.heap);
    }
    printf("50 runs: checksum %lld\n", (long long)check);
    free(held);
    free(draws);
    return 0;
}
