// LeetCode #2011: Final Value of Variable After Performing Operations -- the
// ★ arm's benchmark, a mirror of final_value.kara. Each operation is its own
// heap string, as a `String` is, compared with `strcmp`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t final_value_after_operations(char **operations, int n) {
    int64_t x = 0;
    for (int i = 0; i < n; i++) {
        const char *op = operations[i];
        if (strcmp(op, "++X") == 0 || strcmp(op, "X++") == 0) x += 1;
        else if (strcmp(op, "--X") == 0 || strcmp(op, "X--") == 0) x -= 1;
    }
    return x;
}

static int64_t seed = 2011;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const char *forms[4] = {"++X", "X++", "--X", "X--"};
    static char *lists[20000][100];
    for (int a = 0; a < 20000; a++) {
        int64_t up = next_random() % 11;
        for (int i = 0; i < 100; i++) {
            int64_t down = next_random() % 10 < up ? 0 : 2;
            lists[a][i] = strdup(forms[down + next_random() % 2]);
        }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int r = 0; r < 10; r++) {
        for (int a = 0; a < 20000; a++) {
            int64_t answer = final_value_after_operations(lists[a], 100);
            calls++;
            sum += answer;
            check = (check * 31 + answer + 100) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
