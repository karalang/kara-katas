// LeetCode #2304: Minimum Path Cost in a Grid -- the bench, the ★ arm in
// Rust. Row by row, each column of the next row takes the least over the
// row before of the cost so far plus the move, plus its own value.

fn min_path_cost(grid: &[Vec<i64>], move_cost: &[Vec<i64>]) -> i64 {
    let n = grid[0].len();
    let mut best = grid[0].clone();
    for r in 1..grid.len() {
        let mut next = vec![i64::MAX; n];
        for j in 0..n {
            for k in 0..n {
                next[j] = next[j].min(best[k] + move_cost[grid[r - 1][k] as usize][j]);
            }
            next[j] += grid[r][j];
        }
        best = next;
    }
    *best.iter().min().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2304;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut tables: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..20 {
        let mut values: Vec<i64> = (0..2500).collect();
        for i in (1..2500usize).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            values.swap(i, j);
        }
        let grid: Vec<Vec<i64>> = (0..50).map(|r| values[r * 50..(r + 1) * 50].to_vec()).collect();
        grids.push(grid);
        let mut table = Vec::new();
        for _ in 0..2500 {
            let mut row = Vec::new();
            for _ in 0..50 {
                row.push(next_random(&mut seed) % 100 + 1);
            }
            table.push(row);
        }
        tables.push(table);
    }
    let mut check: i64 = 0;
    for p in 0..40 {
        for a in 0..20 {
            check = (check * 31 + min_path_cost(&grids[a], &tables[(a + p) % 20])) % 1000000007;
        }
    }
    println!("40 passes over 20 grids of 50 by 50: checksum {}", check);
}
