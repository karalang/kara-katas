// LeetCode #1463 bench in Rust: the ★ arm (the most cherries over each
// pair of robot columns, row by row) on the same 40 grids of 70 by 70.

fn cherry_pickup(grid: &[Vec<i32>]) -> i32 {
    let rows = grid.len();
    let cols = grid[0].len() as i64;
    let mut best = vec![vec![-1i32; cols as usize]; cols as usize];
    best[0][cols as usize - 1] = grid[0][0] + grid[0][cols as usize - 1];
    for r in 1..rows {
        let mut next = vec![vec![-1i32; cols as usize]; cols as usize];
        for a in 0..cols {
            for b in 0..cols {
                if best[a as usize][b as usize] < 0 {
                    continue;
                }
                for da in -1..=1 {
                    for db in -1..=1 {
                        let (x, y) = (a + da, b + db);
                        if x < 0 || x >= cols || y < 0 || y >= cols {
                            continue;
                        }
                        let (x, y) = (x as usize, y as usize);
                        let here = if x == y { grid[r][x] } else { grid[r][x] + grid[r][y] };
                        next[x][y] = next[x][y].max(best[a as usize][b as usize] + here);
                    }
                }
            }
        }
        best = next;
    }
    best.iter().map(|row| *row.iter().max().unwrap()).max().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1463i64;
    let mut grids: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..40 {
        let grid: Vec<Vec<i32>> = (0..70).map(|_| (0..70).map(|_| (next_random(&mut seed) % 101) as i32).collect()).collect();
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for g in 0..40 {
        let cell = (check % 4900) as usize;
        grids[g][cell / 70][cell % 70] = (check % 101) as i32;
        let most = cherry_pickup(&grids[g]) as i64;
        check = (check * 31 + most) % 1000000007;
    }
    println!("40 grids of 70 by 70: checksum {check}");
}
