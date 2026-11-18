// LeetCode #2325: Decode the Message -- the bench, the ★ arm in C. One
// walk over the key's bytes fills a table of 26, each letter's first
// appearance given the next letter of the alphabet, and the message is
// read through it, spaces kept. O(|key| + |message|). The decoded
// message and each rotated key are fresh allocations, as in the others.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *decode_message(const char *key, const char *message) {
    unsigned char table[26] = {0};
    unsigned char next = 'a';
    for (const char *p = key; *p; p++)
        if (*p != ' ' && table[*p - 'a'] == 0)
            table[*p - 'a'] = next++;
    size_t n = strlen(message);
    char *decoded = malloc(n + 1);
    for (size_t i = 0; i < n; i++)
        decoded[i] = message[i] == ' ' ? ' ' : (char)table[message[i] - 'a'];
    decoded[n] = 0;
    return decoded;
}

static int64_t seed = 2325;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char letter(void) {
    int64_t roll = next_random() % 27;
    return roll == 26 ? ' ' : (char)('a' + roll);
}

int main(void) {
    char *keys[100], *messages[100];
    for (int k = 0; k < 100; k++) {
        keys[k] = malloc(2001);
        for (int i = 0; i < 1974; i++)
            keys[k][i] = letter();
        memcpy(keys[k] + 1974, "abcdefghijklmnopqrstuvwxyz", 27);
        messages[k] = malloc(2001);
        for (int i = 0; i < 2000; i++)
            messages[k][i] = letter();
        messages[k][2000] = 0;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 1000; p++)
        for (int64_t k = 0; k < 100; k++) {
            char *decoded = decode_message(keys[k], messages[k]);
            check = (check * 31 + (unsigned char)decoded[p % 2000] + (unsigned char)decoded[(7 * p + k) % 2000]) % 1000000007;
            free(decoded);
            char *rotated = malloc(2001);
            memcpy(rotated, keys[k] + 1, 1999);
            rotated[1999] = keys[k][0];
            rotated[2000] = 0;
            free(keys[k]);
            keys[k] = rotated;
        }
    printf("1000 passes over 100 keys and messages of 2000: checksum %lld\n", (long long)check);
    for (int k = 0; k < 100; k++) {
        free(keys[k]);
        free(messages[k]);
    }
    return 0;
}
