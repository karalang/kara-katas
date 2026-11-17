// LeetCode #2232: Minimize Result by Adding Parentheses to Expression --
// the benchmark's C mirror of parentheses.kara: every place for the two
// parentheses, each number parsed from its piece of the string with
// strtoll, and the first smallest a * (b + c) * d written out with
// snprintf.

#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// the number spelled by s[from..to), as a fresh piece parsed by strtoll
static int64_t parse(const char *s, int from, int to) {
    char piece[16];
    memcpy(piece, s + from, (size_t)(to - from));
    piece[to - from] = 0;
    return strtoll(piece, NULL, 10);
}

static void minimize_result(const char *expression, char *answer) {
    int n = (int)strlen(expression);
    int plus = (int)(strchr(expression, '+') - expression);
    int64_t best = INT64_MAX;
    for (int i = 0; i < plus; i++) {
        for (int j = plus + 2; j <= n; j++) {
            int64_t a = i == 0 ? 1 : parse(expression, 0, i);
            int64_t b = parse(expression, i, plus);
            int64_t c = parse(expression, plus + 1, j);
            int64_t d = j == n ? 1 : parse(expression, j, n);
            int64_t value = a * (b + c) * d;
            if (value < best) {
                best = value;
                snprintf(answer, 16, "%.*s(%.*s+%.*s)%s", i, expression, plus - i, expression + i,
                         j - plus - 1, expression + plus + 1, expression + j);
            }
        }
    }
}

static int64_t seed = 2232;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void draw_expression(char *out) {
    int64_t left = next_random() % 8 + 1;
    int64_t right = next_random() % (9 - left) + 1;
    int64_t k;
    for (k = 0; k < left + right + 1; k++) out[k] = k == left ? '+' : (char)(49 + next_random() % 9);
    out[k] = 0;
}

int main(void) {
    static char expressions[20000][12];
    for (int i = 0; i < 20000; i++) draw_expression(expressions[i]);
    int64_t check = 0;
    char answer[16];
    for (int r = 0; r < 20; r++) {
        // punch: one expression drawn again before each pass over all
        int64_t at = next_random() % 20000;
        draw_expression(expressions[at]);
        for (int i = 0; i < 20000; i++) {
            minimize_result(expressions[i], answer);
            int64_t open = strchr(answer, '(') - answer, close = strchr(answer, ')') - answer;
            check = (check * 31 + (int64_t)strlen(answer) + open * 11 + close) % 1000000007;
        }
    }
    printf("20 passes over 20000 expressions: checksum %lld\n", (long long)check);
    return 0;
}
