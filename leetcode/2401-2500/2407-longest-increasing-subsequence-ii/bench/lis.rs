// LeetCode #2407: Longest Increasing Subsequence II -- the bench, the ★
// arm in Rust: a bottom-up segment tree over the values, the longest
// ending at x one more than the tree's maximum over x - k to x - 1.

fn length_of_lis(nums: &[i64], k: i64) -> i64 {
    let top = *nums.iter().max().unwrap();
    let mut size = 1i64;
    while size <= top {
        size *= 2;
    }
    let mut tree = vec![0i64; 2 * size as usize];
    let mut best = 0;
    for &x in nums {
        let mut lo = (x - k).max(0) + size;
        let mut hi = x - 1 + size + 1;
        let mut longest = 0;
        while lo < hi {
            if lo % 2 == 1 {
                longest = longest.max(tree[lo as usize]);
                lo += 1;
            }
            if hi % 2 == 1 {
                hi -= 1;
                longest = longest.max(tree[hi as usize]);
            }
            lo /= 2;
            hi /= 2;
        }
        let mut at = (x + size) as usize;
        tree[at] = tree[at].max(longest + 1);
        best = best.max(longest + 1);
        at /= 2;
        while at > 0 {
            tree[at] = tree[2 * at].max(tree[2 * at + 1]);
            at /= 2;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2407;
    let arrays: Vec<Vec<i64>> = (0..5)
        .map(|_| (0..100000).map(|_| 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000).collect())
        .collect();
    let mut check: i64 = 0;
    for p in 0..4 {
        let mut k = 1;
        for nums in &arrays {
            check = (check * 31 + length_of_lis(nums, k) + p) % 1000000007;
            k *= 10;
        }
    }
    println!("4 passes over 5 arrays of 10^5 values: checksum {}", check);
}
