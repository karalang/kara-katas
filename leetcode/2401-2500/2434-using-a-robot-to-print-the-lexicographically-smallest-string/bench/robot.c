// LeetCode #2434: Using a Robot to Print the Lexicographically Smallest
// String -- the bench, the ★ arm: the letters left counted, a pointer at
// the smallest with a count, and `t` popped after each push while its
// top is no larger.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    unsigned char *data;
    int64_t len, cap;
} Bytes;

static void push(Bytes *v, unsigned char x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap);
    }
    v->data[v->len++] = x;
}

static Bytes robot_with_string(const unsigned char *b, int64_t n) {
    int64_t left[26] = {0};
    for (int64_t i = 0; i < n; i++) left[b[i] - 'a']++;
    int64_t smallest = 0;
    Bytes t = {0, 0, 0}, paper = {0, 0, 0};
    for (int64_t i = 0; i < n; i++) {
        push(&t, b[i]);
        left[b[i] - 'a']--;
        while (smallest < 26 && left[smallest] == 0) smallest++;
        while (t.len > 0 && t.data[t.len - 1] - 'a' <= smallest) push(&paper, t.data[--t.len]);
    }
    free(t.data);
    return paper;
}

static int64_t seed = 2434;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    unsigned char *word = malloc(n);
    for (int64_t i = 0; i < n; i++) word[i] = 'a' + next_random() % 8;
    int64_t check = 0;
    for (int64_t p = 0; p < 300; p++) {
        word[(p * 7919) % n] = 'a' + p % 8;
        Bytes paper = robot_with_string(word, n);
        for (int64_t i = 0; i < paper.len; i++) check = (check * 31 + paper.data[i]) % 1000000007;
        free(paper.data);
    }
    printf("300 passes over 10^5 letters: checksum %lld\n", (long long)check);
    free(word);
    return 0;
}
