// LeetCode #2708: Maximum Strength of a Group -- the bench (strength.kara
// in Rust): every non-zero number multiplied in, and an odd negative,
// the one nearest zero, divided back out.

fn max_strength(nums: &[i64]) -> i64 {
    if nums.len() == 1 {
        return nums[0];
    }
    let mut product: i64 = 1;
    let mut taken = 0;
    let mut negatives = 0;
    let mut nearest: i64 = -10;
    for &v in nums.iter() {
        if v != 0 {
            product *= v;
            taken += 1;
        }
        if v < 0 {
            negatives += 1;
            nearest = nearest.max(v);
        }
    }
    if negatives % 2 == 1 {
        product /= nearest;
        taken -= 1;
    }
    if taken > 0 { product } else { 0 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let groups = 1000000;
    let rounds = 10;
    let mut seed: i64 = 2708;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..groups {
        let n = next_random(&mut seed) % 13 + 1;
        all.push((0..n).map(|_| next_random(&mut seed) % 19 - 9).collect());
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in all.iter() {
            let strength = max_strength(nums);
            sum += strength % 1000;
            check = (check * 31 + (strength % 1000000007 + 1000000007) % 1000000007 + r) % 1000000007;
        }
    }
    println!("{} groups of 1 to 13, {} rounds: strengths mod 1000 sum to {}, checksum {}", groups, rounds, sum, check);
}
