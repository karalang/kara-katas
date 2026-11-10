// LeetCode #2076: Process Restricted Friend Requests -- C mirror of the ★
// arm's benchmark (friends.kara): 400 problems of 1000 people, 1000
// restrictions and 1000 requests; a union-find of parents in an array,
// found with path halving, every restriction tried against a request
// between two groups.
#include <stdio.h>
#include <stdlib.h>

static long long seed = 2076;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_pairs(long long n, long long count, long long *pairs) {
    for (long long i = 0; i < count; i++) {
        long long a = next_random() % n;
        long long b = (a + 1 + next_random() % (n - 1)) % n;
        pairs[2 * i] = a;
        pairs[2 * i + 1] = b;
    }
}

static long long find(long long *parent, long long x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static void friend_requests(long long n, const long long *restrictions, long long r,
                            const long long *requests, long long m, unsigned char *answers) {
    long long *parent = malloc(sizeof(long long) * n);
    for (long long i = 0; i < n; i++) parent[i] = i;
    for (long long j = 0; j < m; j++) {
        long long a = find(parent, requests[2 * j]);
        long long b = find(parent, requests[2 * j + 1]);
        int allowed = 1;
        if (a != b) {
            for (long long k = 0; k < r; k++) {
                long long x = find(parent, restrictions[2 * k]);
                long long y = find(parent, restrictions[2 * k + 1]);
                if ((x == a && y == b) || (x == b && y == a)) {
                    allowed = 0;
                    break;
                }
            }
            if (allowed) parent[a] = b;
        }
        answers[j] = (unsigned char)allowed;
    }
    free(parent);
}

int main(void) {
    long long total = 0, check = 0;
    long long *restrictions = malloc(sizeof(long long) * 2000);
    long long *requests = malloc(sizeof(long long) * 2000);
    unsigned char *answers = malloc(1000);
    for (int t = 0; t < 400; t++) {
        random_pairs(1000, 1000, restrictions);
        random_pairs(1000, 1000, requests);
        friend_requests(1000, restrictions, 1000, requests, 1000, answers);
        for (int j = 0; j < 1000; j++) {
            long long bit = answers[j];
            total += bit;
            check = (check * 3 + bit + 1) % 1000000007;
        }
    }
    printf("400 problems: %lld accepted, checksum %lld\n", total, check);
    free(restrictions);
    free(requests);
    free(answers);
    return 0;
}
