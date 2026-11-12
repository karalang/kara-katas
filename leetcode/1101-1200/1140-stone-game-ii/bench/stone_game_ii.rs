// LeetCode #1140: Stone Game II -- the bench in Rust, the ★ arm's algorithm.

fn stone_game_ii(piles: &[i64]) -> i64 {
    let n = piles.len();
    let mut left = vec![0i64; n + 1];
    for i in (0..n).rev() {
        left[i] = left[i + 1] + piles[i];
    }
    let mut best = vec![vec![0i64; n + 1]; n + 1];
    for i in (0..n).rev() {
        for m in 1..n + 1 {
            if i + 2 * m >= n {
                best[i][m] = left[i];
            } else {
                let mut most = 0;
                for x in 1..2 * m + 1 {
                    most = most.max(left[i] - best[i + x][m.max(x)]);
                }
                best[i][m] = most;
            }
        }
    }
    best[0][1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1140;
    let mut rows: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let row: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 10000 + 1).collect();
        rows.push(row);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..100 {
        for r in 0..20 {
            let at = (next_random(&mut seed) % 100) as usize;
            rows[r][at] = next_random(&mut seed) % 10000 + 1;
            let answer = stone_game_ii(&rows[r]);
            total += answer;
            check = (check * 131 + answer + 1) % 1000000007;
        }
    }
    println!("100 rounds over 20 rows of 100 piles: answers total {total}, checksum {check}");
}
