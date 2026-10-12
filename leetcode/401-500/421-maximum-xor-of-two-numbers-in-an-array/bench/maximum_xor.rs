// Benchmark for #421: mirror of maximum_xor.kara (prefix bits), with
// std's HashSet (SipHash-1-3, as Kāra's Set).
use std::collections::HashSet;

fn find_maximum_xor(nums: &[i64]) -> i64 {
    let mut answer = 0;
    let mut mask = 0;
    let mut bit = 30;
    while bit >= 0 {
        mask |= 1 << bit;
        let mut prefixes: HashSet<i64> = HashSet::new();
        for &x in nums {
            prefixes.insert(x & mask);
        }
        let candidate = answer | (1 << bit);
        for &p in &prefixes {
            if prefixes.contains(&(p ^ candidate)) {
                answer = candidate;
                break;
            }
        }
        bit -= 1;
    }
    answer
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random31(seed: &mut i64) -> i64 {
    let high = step(seed);
    let low = step(seed);
    let bit = step(seed) % 2;
    high * 65536 + low * 2 + bit
}

fn main() {
    let rounds: i64 = std::env::args().nth(1).map_or(100, |s| s.parse().unwrap());
    let n: i64 = 20000;
    let mut seed: i64 = 421;
    let mut nums: Vec<i64> = (0..n).map(|_| random31(&mut seed)).collect();
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        nums[(r * 7919 % n) as usize] = random31(&mut seed);
        let answer = find_maximum_xor(&nums);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{rounds} rounds on {n} numbers: total {total}, checksum {checksum}");
}
