// LeetCode #1307 bench in C: the ★ arm (the sum done a column at a time from
// the right with its carry, the result's letter fixed by each column's sum)
// on the same 40 passes of 50 puzzles.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    // each word and the result as letter numbers, rightmost first
    int words[6][8];
    int lens[6];
    int count;
    int result[8];
    int result_len;
    bool leads[10];
    int digit[10];
    bool taken[10];
} Puzzle;

static bool solve(Puzzle *p, int col, int row, int64_t sum) {
    if (col == p->result_len) return sum == 0;
    if (row == p->count) {
        int letter = p->result[col];
        int d = (int)(sum % 10);
        if (p->digit[letter] >= 0) return p->digit[letter] == d && solve(p, col + 1, 0, sum / 10);
        if (p->taken[d] || (d == 0 && p->leads[letter])) return false;
        p->digit[letter] = d;
        p->taken[d] = true;
        bool ok = solve(p, col + 1, 0, sum / 10);
        p->digit[letter] = -1;
        p->taken[d] = false;
        return ok;
    }
    if (col >= p->lens[row]) return solve(p, col, row + 1, sum);
    int letter = p->words[row][col];
    if (p->digit[letter] >= 0) return solve(p, col, row + 1, sum + p->digit[letter]);
    for (int d = 0; d < 10; d++) {
        if (p->taken[d] || (d == 0 && p->leads[letter])) continue;
        p->digit[letter] = d;
        p->taken[d] = true;
        bool ok = solve(p, col, row + 1, sum + d);
        p->digit[letter] = -1;
        p->taken[d] = false;
        if (ok) return true;
    }
    return false;
}

static bool is_solvable(char words[][8], int count, const char *result) {
    int rlen = (int)strlen(result);
    for (int w = 0; w < count; w++)
        if ((int)strlen(words[w]) > rlen) return false;
    Puzzle p;
    int number[26];
    for (int k = 0; k < 26; k++) number[k] = -1;
    int letters = 0;
    for (int t = 0; t <= count; t++) {
        const char *text = t < count ? words[t] : result;
        int len = (int)strlen(text);
        int row[8];
        for (int k = 0; k < len; k++) {
            int c = text[k] - 'A';
            if (number[c] < 0) {
                number[c] = letters;
                p.leads[letters] = false;
                letters++;
            }
            row[k] = number[c];
        }
        if (len > 1) p.leads[row[0]] = true;
        int *dst = t < count ? p.words[t] : p.result;
        for (int k = 0; k < len; k++) dst[k] = row[len - 1 - k];
        if (t < count) p.lens[t] = len; else p.result_len = len;
    }
    p.count = count;
    for (int k = 0; k < 10; k++) {
        p.digit[k] = -1;
        p.taken[k] = false;
    }
    return solve(&p, 0, 0, 0);
}

static int64_t seed;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int64_t pass = 0; pass < 40; pass++) {
        seed = check;
        int64_t solvable = 0;
        for (int p = 0; p < 50; p++) {
            char letter[10] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'};
            for (int k = 9; k >= 1; k--) {
                int j = (int)(next_random() % (k + 1));
                char tmp = letter[k];
                letter[k] = letter[j];
                letter[j] = tmp;
            }
            int count = 2 + (int)(next_random() % 4);
            int64_t numbers[6];
            int64_t total = 0;
            for (int w = 0; w < count; w++) {
                int digits = 1 + (int)(next_random() % 6);
                int64_t low = 1;
                for (int k = 1; k < digits; k++) low *= 10;
                numbers[w] = digits == 1 ? next_random() % 10 : low + next_random() % (9 * low);
                total += numbers[w];
            }
            numbers[count] = total;
            char texts[6][8];
            for (int w = 0; w <= count; w++) {
                char buf[24];
                snprintf(buf, sizeof buf, "%lld", (long long)numbers[w]);
                int len = (int)strlen(buf);
                for (int k = 0; k < len; k++) texts[w][k] = letter[buf[k] - '0'];
                texts[w][len] = '\0';
            }
            char result[8];
            strcpy(result, texts[count]);
            if (p % 2 == 1) {
                int len = (int)strlen(result);
                int at = (int)(next_random() % len);
                result[at] = letter[next_random() % 10];
            }
            if (is_solvable(texts, count, result)) solvable++;
        }
        check = (check * 31 + solvable + pass) % 1000000007;
    }
    printf("40 passes of 50 puzzles: checksum %lld\n", (long long)check);
    return 0;
}
