// LeetCode #2217: Find Palindrome With Fixed Length -- bench mirror of
// palindrome.kara: the q-th half is 10^(half - 1) + q - 1, mirrored by
// arithmetic, the middle digit of an odd length used once.
#include <stdio.h>
#include <stdlib.h>

static long *kth_palindrome(const long *queries, long k, long int_length) {
    long half = (int_length + 1) / 2;
    long low = 1;
    for (long i = 1; i < half; i++) low *= 10;
    long *answer = malloc(k * sizeof(long));
    for (long i = 0; i < k; i++) {
        long first = low + queries[i] - 1;
        if (first >= low * 10) {
            answer[i] = -1;
            continue;
        }
        long palindrome = first;
        long rest = int_length % 2 == 1 ? first / 10 : first;
        while (rest > 0) {
            palindrome = palindrome * 10 + rest % 10;
            rest /= 10;
        }
        answer[i] = palindrome;
    }
    return answer;
}

static long seed = 2217;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// a draw of 30 bits, since one draw stops at 32767
static long wide_random(void) {
    long high = next_random();
    return high * 32768 + next_random();
}

// queries up to twice the count of palindromes of the length, so about
// half of them have none
static long query(long length) {
    long count = 9;
    for (long i = 0; i < (length - 1) / 2; i++) count *= 10;
    return wide_random() % (2 * count) + 1;
}

#define A 30
#define N 50000
static long lists[A][N];

int main(void) {
    for (int a = 0; a < A; a++) {
        // 5 * 10^4 queries for each length from 1 to 15 in turn
        long length = a % 15 + 1;
        for (long i = 0; i < N; i++) lists[a][i] = query(length);
    }
    long check = 0;
    for (int a = 0; a < A; a++) {
        long length = a % 15 + 1;
        for (long r = 0; r < 10; r++) {
            // punch: one query is drawn again before each answer
            lists[a][r * 4999] = query(length);
            long *ps = kth_palindrome(lists[a], N, length);
            for (long i = 0; i < N; i++) check = (check * 31 + ps[i] + 1) % 1000000007;
            free(ps);
        }
    }
    printf("30 lists of 5 * 10^4 queries, 10 punches: checksum %ld\n", check);
    return 0;
}
