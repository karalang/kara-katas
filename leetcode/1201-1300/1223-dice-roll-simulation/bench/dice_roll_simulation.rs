// LeetCode #1223 bench, Rust mirror of the Kāra ★ arm: count the sequences
// by their last face and run length, for 50 random sets of limits at
// n = 5000; checksum of the answers.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn die_simulator(n: i64, roll_max: &[i64]) -> i64 {
    let modulus: i64 = 1_000_000_007;
    let mut count = vec![vec![0i64; 15]; 6];
    for f in 0..6 {
        count[f][0] = 1;
    }
    for _ in 1..n {
        let mut next = vec![vec![0i64; 15]; 6];
        for f in 0..6 {
            for r in 0..roll_max[f] as usize {
                let c = count[f][r];
                if c == 0 {
                    continue;
                }
                for g in 0..6 {
                    if g != f {
                        next[g][0] = (next[g][0] + c) % modulus;
                    } else if (r as i64) + 1 < roll_max[f] {
                        next[f][r + 1] = (next[f][r + 1] + c) % modulus;
                    }
                }
            }
        }
        count = next;
    }
    let mut total = 0;
    for f in 0..6 {
        for r in 0..15 {
            total = (total + count[f][r]) % modulus;
        }
    }
    total
}

fn main() {
    let mut seed: i64 = 1223;
    let mut check: i64 = 0;
    for _ in 0..50 {
        let roll_max: Vec<i64> = (0..6).map(|_| next_random(&mut seed) % 15 + 1).collect();
        check = (check * 131 + die_simulator(5000, &roll_max)) % 1000000007;
    }
    println!("50 sets of limits at n = 5000: checksum {}", check);
}
