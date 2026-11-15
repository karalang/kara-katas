// LeetCode #2151: Maximum Good People Based on Statements -- the
// benchmark's Rust mirror of statements.kara.

fn maximum_good(statements: &[Vec<i64>]) -> i64 {
    let n = statements.len();
    let mut best = 0;
    for mask in 0..(1i64 << n) {
        let mut holds = true;
        for i in 0..n {
            if (mask >> i) & 1 == 1 {
                for j in 0..n {
                    let say = statements[i][j];
                    if say != 2 && say != (mask >> j) & 1 {
                        holds = false;
                    }
                }
            }
        }
        if holds {
            best = best.max(mask.count_ones() as i64);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2151;
    let n: i64 = 15;
    let mut villages: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..4 {
        let hidden = next_random(&mut seed) % (1 << n);
        let mut statements: Vec<Vec<i64>> = Vec::new();
        for i in 0..n {
            let mut row: Vec<i64> = Vec::new();
            for j in 0..n {
                let say = if i == j {
                    2
                } else if (hidden >> i) & 1 == 1 {
                    if next_random(&mut seed) % 3 == 0 { 2 } else { (hidden >> j) & 1 }
                } else {
                    next_random(&mut seed) % 3
                };
                row.push(say);
            }
            statements.push(row);
        }
        villages.push(statements);
    }
    let mut total = 0;
    let mut check = 0;
    for round in 0..25 {
        for v in 0..4 {
            let i = next_random(&mut seed) % n;
            let j = (i + 1 + next_random(&mut seed) % (n - 1)) % n;
            villages[v][i as usize][j as usize] = next_random(&mut seed) % 3;
            let good = maximum_good(&villages[v]);
            total += good;
            check = (check * 31 + good + round) % 1000000007;
        }
    }
    println!("100 solves: {} good in all, checksum {}", total, check);
}
