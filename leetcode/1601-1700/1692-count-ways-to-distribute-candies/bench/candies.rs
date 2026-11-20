// LeetCode #1692: Count Ways to Distribute Candies -- the bench's Rust
// mirror: the ★ arm on 200 problems of 1000 candies, each with a random
// number of bags up to 1000, all drawn first, each answered 8 times.

fn ways_to_distribute(n: i32, k: i32) -> i32 {
    let modulus: i64 = 1000000007;
    let k = k as usize;
    let mut ways = vec![0i64; k + 1];
    ways[0] = 1;
    for i in 1..=n as usize {
        for j in (1..=i.min(k)).rev() {
            ways[j] = (j as i64 * ways[j] + ways[j - 1]) % modulus;
        }
        ways[0] = 0;
    }
    ways[k] as i32
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 200;
    let rounds = 8;
    let n: i64 = 1000;
    let mut seed = 1692;
    let mut bags: Vec<i32> = Vec::new();
    for _ in 0..count {
        bags.push((next_random(&mut seed) % n + 1) as i32);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &k in bags.iter() {
            let answer = ways_to_distribute(n as i32, k) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} problems of {n} candies, {rounds} rounds: answers sum to {total}, checksum {check}");
}
