// Benchmark for #640: mirror of solve_the_equation.kara (the ★ arm: each
// side read once into a count of x and a constant) on the same workload.
// The answer is written into a caller's buffer, as the Kāra builds a
// String.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROUNDS 200000

static void side(const char *text, int64_t n, int64_t *xs, int64_t *constant) {
    *xs = 0;
    *constant = 0;
    int64_t i = 0;
    while (i < n) {
        int64_t sign = 1;
        if (text[i] == '+' || text[i] == '-') {
            if (text[i] == '-') {
                sign = -1;
            }
            i++;
        }
        int64_t value = 0;
        int64_t digits = 0;
        while (i < n && text[i] >= '0' && text[i] <= '9') {
            value = value * 10 + (text[i] - '0');
            digits++;
            i++;
        }
        if (i < n && text[i] == 'x') {
            *xs += sign * (digits == 0 ? 1 : value);
            i++;
        } else {
            *constant += sign * value;
        }
    }
}

static void solve_equation(const char *equation, char *out, size_t cap) {
    int64_t n = (int64_t)strlen(equation);
    int64_t eq = 0;
    while (equation[eq] != '=') {
        eq++;
    }
    int64_t a, b, c, d;
    side(equation, eq, &a, &b);
    side(equation + eq + 1, n - eq - 1, &c, &d);
    if (a == c) {
        snprintf(out, cap, "%s", b == d ? "Infinite solutions" : "No solution");
    } else {
        snprintf(out, cap, "x=%lld", (long long)((d - b) / (a - c)));
    }
}

static int64_t seed = 640;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *random_side(int terms, int64_t *xs, int64_t *constant) {
    char *text = malloc(8 * terms + 1);
    size_t len = 0;
    *xs = 0;
    *constant = 0;
    for (int t = 0; t < terms; t++) {
        int minus = next_random() % 2 == 0;
        if (minus) {
            text[len++] = '-';
        } else if (t > 0) {
            text[len++] = '+';
        }
        int64_t sign = minus ? -1 : 1;
        int64_t value = next_random() % 100;
        if (next_random() % 2 == 0) {
            len += sprintf(text + len, "%lldx", (long long)value);
            *xs += sign * value;
        } else {
            len += sprintf(text + len, "%lld", (long long)value);
            *constant += sign * value;
        }
    }
    text[len] = 0;
    return text;
}

int main(void) {
    char *equations[20];
    for (int e = 0; e < 20; e++) {
        int64_t a, b, c, d;
        char *left = random_side(125, &a, &b);
        char *right = random_side(125, &c, &d);
        char *text = malloc(strlen(left) + strlen(right) + 32);
        int len = sprintf(text, "%s=%s", left, right);
        if (a != c) {
            int64_t rem = (d - b) % (a - c);
            if (rem > 0) {
                sprintf(text + len, "-%lld", (long long)rem);
            } else if (rem < 0) {
                sprintf(text + len, "+%lld", (long long)-rem);
            }
        }
        free(left);
        free(right);
        equations[e] = text;
    }
    int64_t solved = 0;
    int64_t sum = 0;
    char answer[32];
    for (int64_t round = 0; round < ROUNDS; round++) {
        solve_equation(equations[round % 20], answer, sizeof answer);
        if (answer[0] == 'x' && answer[1] == '=') {
            solved++;
            sum += strtoll(answer + 2, NULL, 10);
        }
    }
    printf("20 equations, %d rounds: %lld solved, x adding to %lld\n", ROUNDS, (long long)solved, (long long)sum);
    for (int e = 0; e < 20; e++) {
        free(equations[e]);
    }
    return 0;
}
