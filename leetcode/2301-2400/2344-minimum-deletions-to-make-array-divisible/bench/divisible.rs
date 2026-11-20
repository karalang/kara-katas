// LeetCode #2344: Minimum Deletions to Make Array Divisible -- the bench,
// the ★ arm in Rust: the gcd of numsDivide, then nums sorted and scanned
// for the first value that divides it.

fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        (a, b) = (b, a % b);
    }
    a
}

fn min_operations(nums: &[i64], nums_divide: &[i64]) -> i64 {
    let mut g = 0;
    for &x in nums_divide {
        g = gcd(g, x);
    }
    let mut sorted = nums.to_vec();
    sorted.sort();
    for i in 0..sorted.len() {
        if g % sorted[i] == 0 {
            return i as i64;
        }
    }
    -1
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647
}

fn main() {
    let mut cases: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for a in 0..10i64 {
        let nums: Vec<i64> = (0..100000i64).map(|i| scrambled(a * 100000 + i) % 1000000 + 1).collect();
        let base = nums[(a * 7919 % 100000) as usize];
        let nums_divide: Vec<i64> = (0..10000i64).map(|i| base * (scrambled(a * 10000 + i + 7) % 1000 + 1)).collect();
        cases.push((nums, nums_divide));
    }
    let mut check = 0i64;
    for p in 0..20i64 {
        for (nums, nums_divide) in &cases {
            check = (check * 31 + min_operations(nums, nums_divide) + p) % 1000000007;
        }
    }
    println!("20 passes over 10 cases of 10^5 values against 10^4: checksum {}", check);
}
