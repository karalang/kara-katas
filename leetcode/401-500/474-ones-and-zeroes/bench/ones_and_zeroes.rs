// Benchmark for #474: Rust mirror of the ★ arm (0/1 knapsack with two
// budgets, one table); see ones_and_zeroes.kara.

fn count_zeros(s: &str) -> i64 {
    let mut zeros = 0;
    for c in s.chars() {
        if c == '0' {
            zeros += 1;
        }
    }
    zeros
}

fn find_max_form(strs: &[String], m: i64, n: i64) -> i64 {
    let mut best = vec![vec![0i64; (n + 1) as usize]; (m + 1) as usize];
    for s in strs {
        let zeros = count_zeros(s);
        let ones = s.len() as i64 - zeros;
        let mut i = m;
        while i >= zeros {
            let mut j = n;
            while j >= ones {
                let take = best[(i - zeros) as usize][(j - ones) as usize] + 1;
                if take > best[i as usize][j as usize] {
                    best[i as usize][j as usize] = take;
                }
                j -= 1;
            }
            i -= 1;
        }
    }
    best[m as usize][n as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 474;
    let mut strs: Vec<String> = Vec::new();
    for _ in 0..600 {
        let size = 1 + next_random(&mut seed) % 100;
        let lean = next_random(&mut seed) % 3;
        let mut s = String::new();
        for _ in 0..size {
            let r = next_random(&mut seed) % 4;
            let zero = if lean == 0 { r != 0 } else if lean == 1 { r == 0 } else { r < 2 };
            s.push(if zero { '0' } else { '1' });
        }
        strs.push(s);
    }
    let rounds = 300;
    let mut total = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let m = 50 + next_random(&mut seed) % 51;
        let n = 50 + next_random(&mut seed) % 51;
        let got = find_max_form(&strs, m, n);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    println!("{} rounds on 600 strings: {} chosen, checksum {}", rounds, total, checksum);
}
