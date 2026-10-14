// Benchmark for #583: Rust mirror of the ★ arm (the longest common
// subsequence); see min_distance.kara. Each word is collected into a
// `Vec<char>` and the table is a `Vec<Vec<i64>>`, as in the Kāra arm.

fn min_distance(word1: String, word2: String) -> i64 {
    let a: Vec<char> = word1.chars().collect();
    let b: Vec<char> = word2.chars().collect();
    let m = a.len();
    let n = b.len();
    let mut lcs = vec![vec![0i64; n + 1]; m + 1];
    for i in 1..=m {
        for j in 1..=n {
            if a[i - 1] == b[j - 1] {
                lcs[i][j] = lcs[i - 1][j - 1] + 1;
            } else {
                lcs[i][j] = lcs[i - 1][j].max(lcs[i][j - 1]);
            }
        }
    }
    m as i64 + n as i64 - 2 * lcs[m][n]
}

// ---- benchmark --------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(len: i64, letters: i64, seed: &mut i64) -> String {
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let mut s = String::new();
    for _ in 0..len {
        let k = (next_random(seed) % letters) as usize;
        s.push_str(&alphabet[k..k + 1]);
    }
    s
}

fn main() {
    let count: i64 = 40;
    let rounds: i64 = 30;
    let mut seed: i64 = 583;
    let mut firsts: Vec<String> = Vec::new();
    let mut seconds: Vec<String> = Vec::new();
    for _ in 0..count {
        let letters = 2 + next_random(&mut seed) % 25;
        firsts.push(word(500, letters, &mut seed));
        seconds.push(word(500, letters, &mut seed));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let p = ((round * 7 + g) % count) as usize;
            let got = min_distance(firsts[p].clone(), seconds[p].clone());
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    println!("{} pairs of 500 letters, {} rounds: {} deletions, checksum {}", count, rounds, total, checksum);
}
