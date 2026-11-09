// LeetCode #2037: Minimum Number of Moves to Seat Everyone -- the ★ arm in
// C, the same algorithm and workload as seats.kara: both lists copied and
// sorted (a stable merge sort, as Kāra's and Rust's `sort` are), the k-th
// seat paired with the k-th student, the distances summed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void merge_sort(int64_t *v, int64_t *tmp, int n) {
    if (n < 2) return;
    int mid = n / 2;
    merge_sort(v, tmp, mid);
    merge_sort(v + mid, tmp, n - mid);
    int i = 0, j = mid, k = 0;
    while (i < mid && j < n) tmp[k++] = v[j] < v[i] ? v[j++] : v[i++];
    while (i < mid) tmp[k++] = v[i++];
    while (j < n) tmp[k++] = v[j++];
    memcpy(v, tmp, n * sizeof(int64_t));
}

static int64_t min_moves_to_seat(int64_t *seats, int64_t *students, int n) {
    int64_t tmp[100];
    merge_sort(seats, tmp, n);
    merge_sort(students, tmp, n);
    int64_t moves = 0;
    for (int k = 0; k < n; k++) moves += llabs(seats[k] - students[k]);
    return moves;
}

static int64_t seed = 2037;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t seats[2000][100], students[2000][100];
    for (int r = 0; r < 2000; r++) {
        for (int i = 0; i < 100; i++) seats[r][i] = next_random() % 100 + 1;
        for (int i = 0; i < 100; i++) students[r][i] = next_random() % 100 + 1;
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t round = 0; round < 25; round++) {
        for (int64_t r = 0; r < 2000; r++) {
            int64_t at = (round * 37 + r * 11) % 100;
            seats[r][at] = seats[r][at] % 100 + 1;
            int64_t a[100], b[100];
            memcpy(a, seats[r], sizeof a);
            memcpy(b, students[r], sizeof b);
            int64_t answer = min_moves_to_seat(a, b, 100);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
