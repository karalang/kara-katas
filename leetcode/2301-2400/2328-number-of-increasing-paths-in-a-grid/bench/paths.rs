// LeetCode #2328: Number of Increasing Paths in a Grid -- the bench, the
// ★ arm in Rust. The cells sorted by value, largest first, and each
// cell's count of paths one plus its larger neighbours' counts, all of
// them already done. O(m n log(m n)).

const MOD: i64 = 1000000007;

fn count_paths(grid: &Vec<Vec<i64>>) -> i64 {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let mut cells: Vec<(i64, i64, i64)> = Vec::new();
    for r in 0..m {
        for c in 0..n {
            cells.push((grid[r as usize][c as usize], r, c));
        }
    }
    cells.sort();
    cells.reverse();
    let moves = [(0i64, 1i64), (1, 0), (0, -1), (-1, 0)];
    let mut from = vec![vec![1i64; n as usize]; m as usize];
    let mut total = 0i64;
    for &(value, r, c) in cells.iter() {
        for &(dr, dc) in moves.iter() {
            let (nr, nc) = (r + dr, c + dc);
            if nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr as usize][nc as usize] > value {
                from[r as usize][c as usize] = (from[r as usize][c as usize] + from[nr as usize][nc as usize]) % MOD;
            }
        }
        total = (total + from[r as usize][c as usize]) % MOD;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2328;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..10 {
        let grid: Vec<Vec<i64>> = (0..250).map(|_| (0..400).map(|_| next_random(&mut seed) % 1000 + 1).collect()).collect();
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for p in 0..3i64 {
        for k in 0..10 {
            check = (check * 31 + count_paths(&grids[k]) + p) % 1000000007;
        }
    }
    println!("3 passes over 10 grids of 10^5 cells: checksum {}", check);
}
