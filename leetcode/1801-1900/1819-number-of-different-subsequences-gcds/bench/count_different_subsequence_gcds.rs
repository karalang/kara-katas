// LeetCode #1819: Number of Different Subsequences GCDs -- the bench in
// Rust: the ★ arm over 100 calls on runs of 50000 to 99999 numbers cut from
// one list of 10^5 numbers from 1 to 2 * 10^5, built once, each run's
// length drawn from the checksum so far.

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn count_different_subsequence_gcds(nums: Vec<i64>) -> i64 {
    let top = *nums.iter().max().unwrap();
    let mut present = vec![false; (top + 1) as usize];
    for &x in nums.iter() {
        present[x as usize] = true;
    }
    let mut count = 0;
    for g in 1..top + 1 {
        let mut d = 0;
        let mut m = g;
        while m <= top && d != g {
            if present[m as usize] {
                d = gcd(d, m);
            }
            m += g;
        }
        if d == g {
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1819;
    let mut base: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let hi = next_random(&mut seed);
        base.push(1 + (hi * 32768 + next_random(&mut seed)) % 200000);
    }
    let mut check: i64 = 0;
    for call in 0..100 {
        let n = (50000 + (check + call) % 50000) as usize;
        check = (check * 31 + count_different_subsequence_gcds(base[..n].to_vec())) % 1000000007;
    }
    println!("100 calls: checksum {}", check);
}
