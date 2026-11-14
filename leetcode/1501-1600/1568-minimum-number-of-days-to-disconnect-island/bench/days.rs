// LeetCode #1568: Minimum Number of Days to Disconnect Island -- bench:
// the ★ arm (each land cell taken away in turn) over 20 grids of 30 by 30,
// built once, all land but for a water cell one time in 20; 5 passes, each
// first turning one cell of every grid over.

fn islands(grid: &[Vec<i64>]) -> i64 {
    let rows = grid.len() as i64;
    let cols = grid[0].len() as i64;
    let mut seen = vec![vec![false; cols as usize]; rows as usize];
    let mut count = 0;
    for r in 0..rows {
        for c in 0..cols {
            if grid[r as usize][c as usize] == 1 && !seen[r as usize][c as usize] {
                count += 1;
                seen[r as usize][c as usize] = true;
                let mut stack = vec![(r, c)];
                while let Some((i, j)) = stack.pop() {
                    for (di, dj) in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
                        let (a, b) = (i + di, j + dj);
                        if a >= 0 && a < rows && b >= 0 && b < cols
                            && grid[a as usize][b as usize] == 1 && !seen[a as usize][b as usize]
                        {
                            seen[a as usize][b as usize] = true;
                            stack.push((a, b));
                        }
                    }
                }
            }
        }
    }
    count
}

fn min_days(grid: &[Vec<i64>]) -> i64 {
    if islands(grid) != 1 {
        return 0;
    }
    let mut grid = grid.to_vec();
    for r in 0..grid.len() {
        for c in 0..grid[0].len() {
            if grid[r][c] == 1 {
                grid[r][c] = 0;
                let split = islands(&grid) != 1;
                grid[r][c] = 1;
                if split {
                    return 1;
                }
            }
        }
    }
    2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n: usize = 30;
    let passes = 5;
    let mut seed = 1568;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..20 {
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..n {
            let row: Vec<i64> = (0..n).map(|_| if next_random(&mut seed) % 20 == 0 { 0 } else { 1 }).collect();
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut check = 0;
    let mut days = [0i64; 3];
    for pass in 0..passes {
        for g in 0..grids.len() {
            let at = (pass * 7919 + g * 104729) % (n * n);
            grids[g][at / n][at % n] = 1 - grids[g][at / n][at % n];
            let answer = min_days(&grids[g]);
            days[answer as usize] += 1;
            check = mix(check, answer);
        }
    }
    println!(
        "{} passes over 20 grids of 30 by 30: {} need 0 days, {} need 1, {} need 2, checksum {}",
        passes, days[0], days[1], days[2], check
    );
}
