// LeetCode #912: Sort an Array -- bench program, Rust.
//
// Heap sort on 500,000 numbers from -5 * 10^4 to 5 * 10^4, built once.
// Each round sorts a copy, folds a sample of the sorted values into a
// checksum and changes one number; 6 rounds.

fn sift_down(a: &mut [i64], start: usize, end: usize) {
    let mut root = start;
    loop {
        let mut child = 2 * root + 1;
        if child >= end {
            return;
        }
        if child + 1 < end && a[child + 1] > a[child] {
            child += 1;
        }
        if a[root] >= a[child] {
            return;
        }
        a.swap(root, child);
        root = child;
    }
}

fn sort_array(nums: &[i64]) -> Vec<i64> {
    let mut a = nums.to_vec();
    let n = a.len();
    for parent in (0..n / 2).rev() {
        sift_down(&mut a, parent, n);
    }
    for end in (1..n).rev() {
        a.swap(0, end);
        sift_down(&mut a, 0, end);
    }
    a
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: usize = 500000;
    let rounds: usize = 6;
    let mut seed: i64 = 912;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(next_random(&mut seed) % 100001 - 50000);
    }
    let mut check: i64 = 0;
    for round in 0..rounds {
        let sorted = sort_array(&nums);
        let mut i = round;
        while i < n {
            check = (check * 31 + sorted[i] + 50000) % 1000000007;
            i += 997;
        }
        nums[round * 7919 % n] = next_random(&mut seed) % 100001 - 50000;
    }
    println!("{} rounds over {} numbers: checksum {}", rounds, n, check);
}
