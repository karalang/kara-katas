// Benchmark: LeetCode #980 Unique Paths III -- the ★ arm, backtracking
// on the grid, on every start and end of an open 4 x 5 grid, LeetCode's
// largest. Mirrors unique_paths_iii.kara, .c, .py and go-seq/.

fn walk(grid: &mut Vec<Vec<i64>>, r: i64, c: i64, left: i64) -> i64 {
    if r < 0
        || c < 0
        || r >= grid.len() as i64
        || c >= grid[0].len() as i64
        || grid[r as usize][c as usize] == -1
    {
        return 0;
    }
    if grid[r as usize][c as usize] == 2 {
        return if left == 0 { 1 } else { 0 };
    }
    grid[r as usize][c as usize] = -1;
    let paths = walk(grid, r + 1, c, left - 1)
        + walk(grid, r - 1, c, left - 1)
        + walk(grid, r, c + 1, left - 1)
        + walk(grid, r, c - 1, left - 1);
    grid[r as usize][c as usize] = 0;
    paths
}

fn unique_paths_iii(grid: &[Vec<i64>]) -> i64 {
    let mut g = grid.to_vec();
    let mut start = (0, 0);
    let mut left = 0;
    for r in 0..g.len() {
        for c in 0..g[0].len() {
            if g[r][c] == 1 {
                start = (r, c);
            } else if g[r][c] != -1 {
                left += 1;
            }
        }
    }
    let (r, c) = start;
    g[r][c] = 0;
    walk(&mut g, r as i64, c as i64, left)
}

fn main() {
    let rounds = 20;
    let rows = 4;
    let cols = 5;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for s in 0..rows * cols {
            for e in 0..rows * cols {
                if s != e {
                    let mut grid = vec![vec![0i64; cols]; rows];
                    grid[s / cols][s % cols] = 1;
                    grid[e / cols][e % cols] = 2;
                    let p = unique_paths_iii(&grid);
                    total += p;
                    check = (check * 31 + p + s as i64) % 1000000007;
                }
            }
        }
    }
    println!(
        "{rounds} rounds over 380 starts and ends of a 4 x 5 grid: {total} paths, checksum {check}"
    );
}
