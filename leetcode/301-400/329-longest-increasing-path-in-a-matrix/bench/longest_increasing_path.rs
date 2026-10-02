// Benchmark workload for LeetCode #329 — Rust mirror of
// longest_increasing_path.kara.
//
// Same workload: a SIDE x SIDE grid built once, then PUNCHES punches, each
// replacing one cell and finding the longest increasing path again with a
// fresh memo.
const SIDE: i64 = 500;
const PUNCHES: i64 = 20;
const MODULUS: i64 = 1_073_741_789;

fn longest_from(matrix: &[Vec<i64>], memo: &mut [Vec<i64>], r: i64, c: i64) -> i64 {
    if memo[r as usize][c as usize] > 0 {
        return memo[r as usize][c as usize];
    }
    let rows = matrix.len() as i64;
    let cols = matrix[0].len() as i64;
    let here = matrix[r as usize][c as usize];
    let mut best = 1;
    for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
        let nr = r + dr;
        let nc = c + dc;
        if nr >= 0 && nr < rows && nc >= 0 && nc < cols && matrix[nr as usize][nc as usize] > here {
            let len = 1 + longest_from(matrix, memo, nr, nc);
            if len > best {
                best = len;
            }
        }
    }
    memo[r as usize][c as usize] = best;
    best
}

fn longest_increasing_path(matrix: &[Vec<i64>]) -> i64 {
    if matrix.is_empty() || matrix[0].is_empty() {
        return 0;
    }
    let mut memo: Vec<Vec<i64>> = matrix.iter().map(|row| vec![0; row.len()]).collect();
    let mut best = 0;
    for r in 0..matrix.len() as i64 {
        for c in 0..matrix[0].len() as i64 {
            let len = longest_from(matrix, &mut memo, r, c);
            if len > best {
                best = len;
            }
        }
    }
    best
}

fn next_rand(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 329;
    let mut grid: Vec<Vec<i64>> = Vec::new();
    for _ in 0..SIDE {
        let mut row = Vec::new();
        for _ in 0..SIDE {
            row.push(next_rand(&mut seed) % 1000);
        }
        grid.push(row);
    }
    let mut sink: i64 = 0;
    for _ in 0..PUNCHES {
        let r = next_rand(&mut seed) % SIDE;
        let c = next_rand(&mut seed) % SIDE;
        grid[r as usize][c as usize] = next_rand(&mut seed) % 1000;
        let len = longest_increasing_path(&grid);
        sink = (sink * 31 + len * 1000003 + r * SIDE + c) % MODULUS;
    }
    println!("sink {}", sink);
}
