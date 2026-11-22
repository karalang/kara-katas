// LeetCode #2859: Sum of Values at Indices With K Set Bits -- the
// bench: the ★ arm over 2000 arrays of 1000 values up to 10^5,
// LeetCode's most, with k up to 10, all drawn first, then each answered
// 100 times.

fn sum_indices_with_k_set_bits(nums: &[i64], k: i64) -> i64 {
    nums.iter().enumerate().filter(|(i, _)| i.count_ones() as i64 == k).map(|(_, &x)| x).sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 2000;
    let rounds = 100;
    let mut seed = 2859;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let k = next_random(&mut seed) % 11;
        let nums: Vec<i64> = (0..1000).map(|_| wide(&mut seed) % 100000 + 1).collect();
        cases.push((nums, k));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (nums, k) in cases.iter() {
            let sum = sum_indices_with_k_set_bits(nums, *k);
            total += sum;
            check = (check * 31 + sum + r) % 1000000007;
        }
    }
    println!("{count} arrays, {rounds} rounds: sums total {total}, checksum {check}");
}
