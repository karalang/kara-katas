// LeetCode #1814: Count Nice Pairs in an Array -- the bench in Rust: the
// ★ arm over 200 calls on runs of 50000 to 99999 numbers cut from one
// array of 10^5, built once, each run's length drawn from the checksum so
// far.
use std::collections::HashMap;

const MOD: i64 = 1000000007;

fn rev(x: i64) -> i64 {
    let mut x = x;
    let mut r = 0;
    while x > 0 {
        r = r * 10 + x % 10;
        x /= 10;
    }
    r
}

fn count_nice_pairs(nums: Vec<i64>) -> i64 {
    let mut seen: HashMap<i64, i64> = HashMap::new();
    let mut pairs = 0;
    for x in nums {
        let d = x - rev(x);
        let c = *seen.get(&d).unwrap_or(&0);
        pairs = (pairs + c) % MOD;
        seen.insert(d, c + 1);
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1814;
    let mut base: Vec<i64> = Vec::new();
    for k in 0..100000 {
        if k % 2 == 0 {
            base.push(next_random(&mut seed) % 10000);
        } else {
            base.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000001);
        }
    }
    let mut check: i64 = 0;
    for call in 0..200 {
        let n = (50000 + (check + call) % 50000) as usize;
        check = (check * 31 + count_nice_pairs(base[..n].to_vec())) % MOD;
    }
    println!("200 calls: checksum {}", check);
}
