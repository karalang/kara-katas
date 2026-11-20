// LeetCode #2341: Maximum Number of Pairs in Array -- the bench, the ★ arm
// in Rust: each value counted in a table of 101, the pairs every count's
// half and the leftovers its parity.

fn number_of_pairs(nums: &[i64]) -> Vec<i64> {
    let mut counts = vec![0i64; 101];
    for &x in nums {
        counts[x as usize] += 1;
    }
    let mut pairs = 0;
    let mut left = 0;
    for &c in &counts {
        pairs += c / 2;
        left += c % 2;
    }
    vec![pairs, left]
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647
}

fn main() {
    let arrays: Vec<Vec<i64>> = (0..10i64)
        .map(|a| (0..100000i64).map(|i| scrambled(a * 100000 + i) % 101).collect())
        .collect();
    let mut check = 0i64;
    for p in 0..50i64 {
        for nums in &arrays {
            let answer = number_of_pairs(nums);
            check = (check * 31 + answer[0] * 101 + answer[1] + p) % 1000000007;
        }
    }
    println!("50 passes over 10 arrays of 10^5 values: checksum {}", check);
}
