// LeetCode #2824: Count Pairs Whose Sum is Less than Target -- the
// bench's Rust mirror of the ★ arm: the numbers sorted, two pointers
// closing in.

fn count_pairs(nums: &[i64], target: i64) -> i64 {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let (mut i, mut j) = (0usize, sorted.len() - 1);
    let mut count = 0;
    while i < j {
        if sorted[i] + sorted[j] < target {
            count += (j - i) as i64;
            i += 1;
        } else {
            j -= 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 200000;
    let rounds = 5;
    let mut seed = 2824;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..50).map(|_| next_random(&mut seed) % 101 - 50).collect();
        let target = next_random(&mut seed) % 101 - 50;
        cases.push((nums, target));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, target) in &cases {
            let a = count_pairs(nums, *target);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{} arrays of 50, {} rounds: {} pairs, checksum {}", count, rounds, total, check);
}
