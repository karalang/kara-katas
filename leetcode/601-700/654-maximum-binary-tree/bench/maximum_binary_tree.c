// Benchmark for #654: a stack of the right spine, as the Kara ★ arm. Each
// tree is freed before the next is built, as the Kara program drops it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static TreeNode **stack;

static TreeNode *construct(const int64_t *nums, int64_t n) {
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        TreeNode *node = malloc(sizeof *node);
        node->val = nums[i];
        node->left = node->right = NULL;
        while (top > 0 && stack[top - 1]->val < nums[i]) node->left = stack[--top];
        if (top > 0) stack[top - 1]->right = node;
        stack[top++] = node;
    }
    return top ? stack[0] : NULL;
}

static void release(TreeNode *node) {
    if (!node) return;
    release(node->left);
    release(node->right);
    free(node);
}

static int64_t seed = 654;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int inputs = 8, rounds = 100;
    int64_t n = 200000;
    int64_t *lists[8];
    stack = malloc(n * sizeof *stack);
    for (int k = 0; k < inputs; k++) {
        int64_t *nums = malloc(n * sizeof *nums);
        for (int64_t i = 0; i < n; i++) nums[i] = i;
        for (int64_t i = n - 1; i > 0; i--) {
            int64_t hi = next_random();
            int64_t j = (hi * 32768 + next_random()) % (i + 1);
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
        lists[k] = nums;
    }
    int64_t checksum = 0;
    for (int r = 0; r < rounds; r++) {
        TreeNode *root = construct(lists[(r * 3) % inputs], n);
        int64_t left = 0, right = 0;
        for (TreeNode *at = root; at; at = at->left) left++;
        for (TreeNode *at = root; at; at = at->right) right++;
        checksum = (checksum * 31 + left * 1000 + right) % 1000000007;
        release(root);
    }
    for (int k = 0; k < inputs; k++) free(lists[k]);
    free(stack);
    printf("%d orders of %lld, %d rounds: checksum %lld\n", inputs, (long long)n, rounds,
           (long long)checksum);
    return 0;
}
