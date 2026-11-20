// LeetCode #1278 bench, in Rust: the ★ arm (the changes for every
// substring, then the fewest for each prefix in each number of pieces) on
// 200 random strings of 100 letters from 2 to 26, each cut into 1 to 100
// pieces, drawn once; 20 rounds, every answer folded into a checksum.

fn palindrome_partition(s: &str, k: i64) -> i64 {
    let c: Vec<char> = s.chars().collect();
    let n = c.len();
    let k = k as usize;
    let mut cost = vec![vec![0i64; n]; n];
    for len in 2..n + 1 {
        for i in 0..n - len + 1 {
            let j = i + len - 1;
            let inner = if len > 2 { cost[i + 1][j - 1] } else { 0 };
            cost[i][j] = inner + if c[i] != c[j] { 1 } else { 0 };
        }
    }
    let unreachable = n as i64 + 1;
    let mut best = vec![vec![unreachable; n + 1]; k + 1];
    best[0][0] = 0;
    for p in 1..k + 1 {
        for j in p..n + 1 {
            for i in p - 1..j {
                let through = best[p - 1][i] + cost[i][j - 1];
                if through < best[p][j] {
                    best[p][j] = through;
                }
            }
        }
    }
    best[k][n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1278i64;
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let mut cases: Vec<(String, i64)> = Vec::new();
    for _ in 0..200 {
        let letters = next_random(&mut seed) % 25 + 2;
        let mut s = String::new();
        for _ in 0..100 {
            let i = (next_random(&mut seed) % letters) as usize;
            s.push_str(&alphabet[i..i + 1]);
        }
        let k = next_random(&mut seed) % 100 + 1;
        cases.push((s, k));
    }
    let mut check = 0i64;
    for round in 0..20 {
        for (s, k) in cases.iter() {
            check = (check * 131 + palindrome_partition(s, *k) + round) % 1000000007;
        }
    }
    println!("20 rounds of 200 strings of 100 letters: checksum {}", check);
}
