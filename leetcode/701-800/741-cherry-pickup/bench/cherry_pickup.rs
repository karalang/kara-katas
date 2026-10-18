// LeetCode #741: Cherry Pickup -- two walkers, one layer at a time.
// Benchmark mirror of the Kara star arm: two walkers go from the near
// corner to the far one together, a cherry on a shared cell counted
// once; keep the best cherries for every pair of rows after k steps
// and build the next layer from it.

fn cherry_pickup(grid: &Vec<Vec<i64>>) -> i64 {
    let n = grid.len();
    let none = -1;
    let mut best: Vec<Vec<i64>> = Vec::new();
    for _ in 0..n {
        let mut row: Vec<i64> = Vec::new();
        for _ in 0..n {
            row.push(none);
        }
        best.push(row);
    }
    if grid[0][0] == -1 {
        return 0;
    }
    best[0][0] = grid[0][0];
    for k in 1..2 * n - 1 {
        let mut next: Vec<Vec<i64>> = Vec::new();
        for _ in 0..n {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..n {
                row.push(none);
            }
            next.push(row);
        }
        let low = if k >= n { k - n + 1 } else { 0 };
        let high = if k < n { k } else { n - 1 };
        for r1 in low..high + 1 {
            for r2 in low..high + 1 {
                let c1 = k - r1;
                let c2 = k - r2;
                if grid[r1][c1] == -1 || grid[r2][c2] == -1 {
                    continue;
                }
                let mut from = none;
                for d1 in 0..2 {
                    for d2 in 0..2 {
                        if r1 >= d1 && r2 >= d2 && best[r1 - d1][r2 - d2] > from {
                            from = best[r1 - d1][r2 - d2];
                        }
                    }
                }
                if from == none {
                    continue;
                }
                let mut here = grid[r1][c1];
                if r2 != r1 {
                    here += grid[r2][c2];
                }
                next[r1][r2] = from + here;
            }
        }
        best = next;
    }
    if best[n - 1][n - 1] == none { 0 } else { best[n - 1][n - 1] }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 741;
    let n: usize = 50;
    let mut grid: Vec<Vec<i64>> = Vec::new();
    for r in 0..n {
        let mut row: Vec<i64> = Vec::new();
        for c in 0..n {
            let corner = (r == 0 && c == 0) || (r == n - 1 && c == n - 1);
            if !corner && next_random(&mut seed) % 10 == 0 {
                row.push(-1);
            } else {
                row.push(next_random(&mut seed) % 2);
            }
        }
        grid.push(row);
    }
    let mut total: i64 = 0;
    for _ in 0..300 {
        for _ in 0..5 {
            let r = (next_random(&mut seed) % n as i64) as usize;
            let c = (next_random(&mut seed) % n as i64) as usize;
            let v = next_random(&mut seed) % 10;
            let corner = (r == 0 && c == 0) || (r == n - 1 && c == n - 1);
            if !corner {
                grid[r][c] = if v == 0 { -1 } else { v % 2 };
            }
        }
        total += cherry_pickup(&grid);
    }
    println!("300 rounds of a 50 by 50 grid: {} cherries in all", total);
}
