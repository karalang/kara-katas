// LeetCode #1262 bench, in Rust: the ★ arm (the best sum with each
// remainder modulo 3, in an `[i64; 3]` copied before each number) on 100
// random lists of 4 * 10^4 numbers from 1 to 10^4 built once, 30 rounds;
// every answer folded into a checksum.

fn max_sum_div_three(nums: &[i64]) -> i64 {
    // -1 marks a remainder no sum has reached yet.
    let mut best: [i64; 3] = [0, -1, -1];
    for &x in nums {
        let before = best;
        for r in 0..3 {
            if before[r] >= 0 {
                let sum = before[r] + x;
                if sum > best[(sum % 3) as usize] {
                    best[(sum % 3) as usize] = sum;
                }
            }
        }
    }
    best[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1262;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100 {
        lists.push((0..40000).map(|_| next_random(&mut seed) % 10000 + 1).collect());
    }
    let mut check: i64 = 0;
    for round in 0..30 {
        for l in 0..100 {
            let best = max_sum_div_three(&lists[l]);
            check = (check * 131 + best + round) % 1000000007;
        }
    }
    println!("30 rounds of 100 lists of 40000: checksum {check}");
}
