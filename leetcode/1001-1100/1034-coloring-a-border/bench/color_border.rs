// LeetCode #1034: Coloring A Border -- bench
// Mirrors ./color_border.kara; see ../README.md § Benchmarks.

fn visit(grid: &[Vec<i64>], r: i64, c: i64, color: i64, seen: &mut Vec<Vec<bool>>, out: &mut Vec<Vec<i64>>) {
    seen[r as usize][c as usize] = true;
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let mut border = false;
    for (dr, dc) in vec![(-1i64, 0i64), (1, 0), (0, -1), (0, 1)].iter() {
        let (nr, nc) = (r + dr, c + dc);
        if nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr as usize][nc as usize] != grid[r as usize][c as usize] {
            border = true;
        } else if !seen[nr as usize][nc as usize] {
            visit(grid, nr, nc, color, seen, out);
        }
    }
    if border {
        out[r as usize][c as usize] = color;
    }
}

fn color_border(grid: &[Vec<i64>], row: i64, col: i64, color: i64) -> Vec<Vec<i64>> {
    let mut seen: Vec<Vec<bool>> = vec![vec![false; grid[0].len()]; grid.len()];
    let mut out = grid.to_vec();
    visit(grid, row, col, color, &mut seen, &mut out);
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let starts = 10;
    let rounds = 20;
    let mut seed = 1034;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut asks: Vec<(usize, i64, i64, i64)> = Vec::new();
    for g in 0..count {
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..50 {
            let mut line: Vec<i64> = Vec::new();
            for _ in 0..50 {
                line.push(if next_random(&mut seed) % 3 == 0 { 2 } else { 1 });
            }
            grid.push(line);
        }
        grids.push(grid);
        for _ in 0..starts {
            let row = next_random(&mut seed) % 50;
            let col = next_random(&mut seed) % 50;
            let color = next_random(&mut seed) % 3 + 1;
            asks.push((g, row, col, color));
        }
    }
    let mut changed: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for &(g, row, col, color) in asks.iter() {
            let grid = &grids[g];
            let painted = color_border(grid, row, col, color);
            for r in 0..50 {
                for c in 0..50 {
                    if painted[r][c] != grid[r][c] {
                        changed += 1;
                        check = (check * 131 + (r * 50 + c) as i64) % 1000000007;
                    }
                }
            }
        }
    }
    println!("{} grids of 50 by 50, {} starts each, {} rounds: {} squares changed, checksum {}", count, starts, rounds, changed, check);
}
