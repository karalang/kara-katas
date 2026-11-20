// LeetCode #1680: Concatenation of Consecutive Binary Numbers -- the bench's
// Rust mirror: the ★ arm on 800 random n up to 100000, all drawn first,
// each answered 5 times.

fn concatenated_binary(n: i32) -> i32 {
    let modulus: i64 = 1000000007;
    let mut value: i64 = 0;
    let mut bits = 0;
    for i in 1..=n as i64 {
        if i & (i - 1) == 0 {
            bits += 1;
        }
        value = ((value << bits) + i) % modulus;
    }
    value as i32
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 800;
    let rounds: i64 = 5;
    let mut seed: i64 = 1680;
    let mut ns: Vec<i32> = Vec::new();
    for _ in 0..count {
        ns.push(((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1) as i32);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &n in &ns {
            let answer = concatenated_binary(n) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} values of n, {} rounds: answers sum to {}, checksum {}", count, rounds, total, check);
}
