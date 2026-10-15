// Benchmark for #664: intervals, by their last letter, as the Kara ★ arm.

fn strange_printer(s: &str) -> i64 {
    let b = s.as_bytes();
    let n = b.len();
    if n == 0 {
        return 0;
    }
    let mut turns = vec![vec![0i64; n]; n];
    for i in (0..n).rev() {
        turns[i][i] = 1;
        for j in i + 1..n {
            let mut best = turns[i][j - 1] + 1;
            for k in i..j {
                if b[k] == b[j] {
                    let between = if k + 1 <= j - 1 { turns[k + 1][j - 1] } else { 0 };
                    best = best.min(turns[i][k] + between);
                }
            }
            turns[i][j] = best;
        }
    }
    turns[0][n - 1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 664;
    let mut texts: Vec<String> = Vec::new();
    for t in 0..64 {
        let letters = 2 + t % 25;
        let mut s = String::new();
        for _ in 0..100 {
            s.push((97 + next_random(&mut seed) % letters) as u8 as char);
        }
        texts.push(s);
    }
    let rounds = 2000i64;
    let mut sum = 0i64;
    for r in 0..rounds {
        let t = strange_printer(&texts[(r % 64) as usize]);
        sum = (sum * 31 + t + r) % 1000000007;
    }
    println!("64 texts of 100 letters, {} rounds: checksum {}", rounds, sum);
}
