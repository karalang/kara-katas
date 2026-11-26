// LeetCode #1775: Equal Sum Arrays With Minimum Number of Operations --
// the bench in C, mirroring min_operations.kara: the gains counted by size
// and the largest taken first.
#include <stdio.h>
#include <stdlib.h>

static int min_operations(const int *nums1, int n1, const int *nums2, int n2) {
    int sum1 = 0, sum2 = 0;
    for (int i = 0; i < n1; i++) sum1 += nums1[i];
    for (int i = 0; i < n2; i++) sum2 += nums2[i];
    if (sum1 == sum2) return 0;
    const int *low = nums1, *high = nums2;
    int nl = n1, nh = n2;
    if (sum1 > sum2) { low = nums2; high = nums1; nl = n2; nh = n1; }
    int gap = abs(sum1 - sum2);
    int gains[6] = {0};
    for (int i = 0; i < nl; i++) gains[6 - low[i]]++;
    for (int i = 0; i < nh; i++) gains[high[i] - 1]++;
    int ops = 0;
    for (int g = 5; g >= 1; g--)
        while (gains[g] > 0 && gap > 0) { gap -= g; gains[g]--; ops++; }
    return gap > 0 ? -1 : ops;
}

static long long seed = 1775;
static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int lists[40][100000];
    for (int r = 0; r < 40; r++) {
        long long low = 1 + next_random() % 3;
        long long high = 4 + next_random() % 3;
        for (int i = 0; i < 100000; i++) lists[r][i] = (int)(low + next_random() % (high - low + 1));
    }
    long long check = 0;
    for (long long call = 0; call < 400; call++) {
        long long a = (check + call) % 40;
        long long b = (check / 40 + call * 7) % 40;
        check = (check * 31 + min_operations(lists[a], 100000, lists[b], 100000) + 1) % 1000000007;
    }
    printf("400 calls over 40 lists: checksum %lld\n", check);
    return 0;
}
