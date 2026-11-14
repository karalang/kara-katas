// LeetCode #1563: Stone Game V -- bench: the ★ arm (every stretch,
// shortest first, every split) over 5 rows of 400 stones of 1 to 10^6,
// built once, each asked twice.
// Rust mirror of stones.kara.

fn stone_game_v(row: &[i64]) -> i64 {
    let n = row.len();
    let mut prefix = vec![0i64; n + 1];
    for i in 0..n {
        prefix[i + 1] = prefix[i] + row[i];
    }
    let mut best = vec![vec![0i64; n]; n];
    for length in 2..=n {
        for i in 0..=n - length {
            let j = i + length - 1;
            let mut most = 0;
            for k in i..j {
                let left = prefix[k + 1] - prefix[i];
                let right = prefix[j + 1] - prefix[k + 1];
                if left < right {
                    most = most.max(left + best[i][k]);
                } else if left > right {
                    most = most.max(right + best[k + 1][j]);
                } else {
                    most = most.max(left + best[i][k].max(best[k + 1][j]));
                }
            }
            best[i][j] = most;
        }
    }
    best[0][n - 1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1563;
    let mut rows: Vec<Vec<i64>> = Vec::new();
    for _ in 0..5 {
        let mut row = Vec::new();
        for _ in 0..400 {
            row.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000 + 1);
        }
        rows.push(row);
    }
    let mut check = 0;
    let mut total = 0;
    for _ in 0..2 {
        for row in &rows {
            let score = stone_game_v(row);
            total += score;
            check = mix(check, score);
        }
    }
    println!("2 passes over 5 rows of 400 stones: {} points, checksum {}", total, check);
}
