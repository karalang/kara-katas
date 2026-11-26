// LeetCode #1399 bench -- C: each number's digit sum by peeling off its
// last digit, the groups' sizes in an array indexed by the sum, and the
// groups of the largest size counted.
#include <stdio.h>

static long long digit_sum(int x) {
    int rest = x;
    long long sum = 0;
    while (rest > 0) {
        sum += rest % 10;
        rest /= 10;
    }
    return sum;
}

static int count_largest_group(int n) {
    int size[37] = {0};
    for (int x = 1; x <= n; x++) size[digit_sum(x)]++;
    int largest = 0;
    for (int s = 0; s < 37; s++)
        if (size[s] > largest) largest = size[s];
    int count = 0;
    for (int s = 0; s < 37; s++)
        if (size[s] == largest) count++;
    return count;
}

int main(void) {
    long long check = 0;
    for (long long r = 0; r < 6000; r++) {
        long long n = 1 + (check + r * 7919) % 10000;
        check = (check * 131 + count_largest_group((int)n)) % 1000000007;
    }
    printf("6000 rounds of n up to 10^4: checksum %lld\n", check);
    return 0;
}
