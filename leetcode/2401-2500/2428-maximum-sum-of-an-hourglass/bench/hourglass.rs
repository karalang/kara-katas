// LeetCode #2428: Maximum Sum of an Hourglass -- the bench, the ★ arm:
// every centre off the border, its seven cells added directly.

fn max_sum(grid: &[Vec<i64>]) -> i64 {
    let m = grid.len();
    let n = grid[0].len();
    let mut best = 0;
    for r in 1..m - 1 {
        for c in 1..n - 1 {
            let sum = grid[r - 1][c - 1] + grid[r - 1][c] + grid[r - 1][c + 1]
                + grid[r][c]
                + grid[r + 1][c - 1] + grid[r + 1][c] + grid[r + 1][c + 1];
            best = best.max(sum);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2428;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..10 {
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..150 {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..150 {
                let a = next_random(&mut seed);
                row.push((a * 32768 + next_random(&mut seed)) % 1000001);
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for p in 0..600i64 {
        for g in 0..10 {
            grids[g][((p * 37) % 150) as usize][((p * 91) % 150) as usize] = (p * 7919) % 1000001;
            check = (check * 31 + max_sum(&grids[g]) + p) % 1000000007;
        }
    }
    println!("600 passes over 10 grids of 150 by 150: checksum {}", check);
}
