// LeetCode #2731: Movement of Robots -- the bench (robots.kara in Rust):
// the places after d seconds, robots passing through each other in
// effect, sorted, each adding its distance to all those before it.

const MOD: i64 = 1000000007;

fn sum_distance(nums: &[i64], s: &str, d: i64) -> i64 {
    let ways = s.as_bytes();
    let mut places: Vec<i64> = Vec::new();
    for i in 0..nums.len() {
        places.push(if ways[i] == b'L' { nums[i] - d } else { nums[i] + d });
    }
    places.sort();
    let mut total: i64 = 0;
    let mut before: i64 = 0;
    for k in 0..places.len() {
        total = (total + k as i64 * places[k] - before) % MOD;
        before += places[k];
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let cases = 10;
    let n: i64 = 100000;
    let rounds = 10;
    let mut seed: i64 = 2731;
    let mut problems: Vec<(Vec<i64>, String, i64)> = Vec::new();
    for _ in 0..cases {
        let mut nums: Vec<i64> = Vec::new();
        let mut at: i64 = -2000000000;
        for _ in 0..n {
            nums.push(at);
            at += (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 40000 + 1;
        }
        for i in (1..n).rev() {
            let j = next_random(&mut seed) % (i + 1);
            nums.swap(i as usize, j as usize);
        }
        let mut s = String::new();
        for _ in 0..n {
            s.push(if next_random(&mut seed) % 2 == 0 { 'L' } else { 'R' });
        }
        let hi = next_random(&mut seed);
        let d = (hi * 32768 + next_random(&mut seed)) % 1000000001;
        problems.push((nums, s, d));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, s, d) in problems.iter() {
            let total = sum_distance(nums, s, *d);
            sum += total;
            check = (check * 31 + total + r) % 1000000007;
        }
    }
    println!("{} cases of {} robots, {} rounds: sums mod p sum to {}, checksum {}", cases, n, rounds, sum, check);
}
