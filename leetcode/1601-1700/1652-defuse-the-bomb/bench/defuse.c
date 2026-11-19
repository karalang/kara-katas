// LeetCode #1652: Defuse the Bomb -- the bench's C mirror: the ★ arm on
// 400 random codes of 100000 numbers from 1 to 100, each with a k from
// -99999 to 99999, all drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CODES 400
#define N 100000

static int32_t *decrypt(const int32_t *code, int64_t n, int32_t k) {
    int32_t *answer = calloc(n, sizeof(int32_t));
    if (k == 0) return answer;
    int64_t start, end;
    if (k > 0) {
        start = 1;
        end = k;
    } else {
        start = n + k;
        end = n - 1;
    }
    int32_t sum = 0;
    for (int64_t j = start; j <= end; j++) sum += code[j % n];
    for (int64_t i = 0; i < n; i++) {
        answer[i] = sum;
        sum -= code[start % n];
        start += 1;
        end += 1;
        sum += code[end % n];
    }
    return answer;
}

static int64_t seed = 1652;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t codes[CODES][N];
    static int32_t ks[CODES];
    for (int c = 0; c < CODES; c++) {
        for (int i = 0; i < N; i++) codes[c][i] = (int32_t)(next_random() % 100 + 1);
        ks[c] = (int32_t)(next_random() % (2 * N - 1) - (N - 1));
    }
    int64_t check = 0, total = 0;
    for (int c = 0; c < CODES; c++) {
        int32_t *answer = decrypt(codes[c], N, ks[c]);
        for (int i = 0; i < N; i++) {
            int64_t x = answer[i];
            total += x;
            check = (check * 31 + x + 1) % 1000000007;
        }
        free(answer);
    }
    printf("400 codes of 100000 numbers: answers sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
