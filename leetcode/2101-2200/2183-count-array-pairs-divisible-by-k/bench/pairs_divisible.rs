// LeetCode #2183: Count Array Pairs Divisible by K -- the benchmark's
// Rust mirror of pairs_divisible.kara, over a slice.

fn gcd(a: i64, b: i64) -> i64 {
    let mut a = a;
    let mut b = b;
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn count_pairs(nums: &[i64], k: i64) -> i64 {
    let mut by_gcd = vec![0i64; (k + 1) as usize];
    for &x in nums {
        by_gcd[gcd(x, k) as usize] += 1;
    }
    let mut divisors: Vec<i64> = Vec::new();
    let mut d = 1i64;
    while d * d <= k {
        if k % d == 0 {
            if by_gcd[d as usize] > 0 {
                divisors.push(d);
            }
            if d * d != k && by_gcd[(k / d) as usize] > 0 {
                divisors.push(k / d);
            }
        }
        d += 1;
    }
    let mut pairs = 0i64;
    for a in 0..divisors.len() {
        for b in a..divisors.len() {
            let g = divisors[a];
            let h = divisors[b];
            if g * h % k == 0 {
                if a == b {
                    pairs += by_gcd[g as usize] * (by_gcd[g as usize] - 1) / 2;
                } else {
                    pairs += by_gcd[g as usize] * by_gcd[h as usize];
                }
            }
        }
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    let b = next_random(seed);
    a * 32768 + b
}

fn main() {
    let mut seed = 2183i64;
    let row: Vec<i64> = (0..1000000).map(|_| big_random(&mut seed) % 100000 + 1).collect();
    let mut check = 0i64;
    for _ in 0..200 {
        let start = (big_random(&mut seed) % 900001) as usize;
        let k = big_random(&mut seed) % 100000 + 1;
        let found = count_pairs(&row[start..start + 100000], k);
        check = (check * 31 + found % 1000000007) % 1000000007;
    }
    println!("200 solves: checksum {}", check);
}
