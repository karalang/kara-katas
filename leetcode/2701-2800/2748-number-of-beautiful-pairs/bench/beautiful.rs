// LeetCode #2748: Number of Beautiful Pairs -- the bench (beautiful.kara
// in Rust): the first digits seen so far counted, each number adding the
// counts of the digits coprime to its last digit.

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn count_beautiful_pairs(nums: &[i64]) -> i64 {
    let mut firsts = [0i64; 10];
    let mut pairs = 0;
    for &x in nums.iter() {
        let last = x % 10;
        for d in 1..10 {
            if gcd(d, last) == 1 {
                pairs += firsts[d as usize];
            }
        }
        let mut first = x;
        while first >= 10 {
            first /= 10;
        }
        firsts[first as usize] += 1;
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20000;
    let rounds = 10;
    let mut seed = 2748;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..100)
            .map(|_| {
                let x = next_random(&mut seed) % 9999 + 1;
                if x % 10 == 0 { x + 1 } else { x }
            })
            .collect();
        lists.push(nums);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in lists.iter() {
            let pairs = count_beautiful_pairs(nums);
            sum += pairs;
            check = (check * 31 + pairs + r) % 1000000007;
        }
    }
    println!("{count} lists of 100 numbers, {rounds} rounds: pairs sum to {sum}, checksum {check}");
}
