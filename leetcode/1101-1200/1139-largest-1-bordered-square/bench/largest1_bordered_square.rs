// LeetCode #1139: Largest 1-Bordered Square -- the bench, the ★ arm's
// algorithm: runs of 1s left and up, each corner's sides tried from the longest down.

fn largest1_bordered_square(grid: &Vec<Vec<i64>>) -> i64 {
    let rows = grid.len();
    let cols = grid[0].len();
    let mut left: Vec<Vec<i64>> = (0..rows).map(|_| vec![0; cols]).collect();
    let mut up: Vec<Vec<i64>> = (0..rows).map(|_| vec![0; cols]).collect();
    for i in 0..rows {
        for j in 0..cols {
            if grid[i][j] == 1 {
                left[i][j] = if j > 0 { left[i][j - 1] + 1 } else { 1 };
                up[i][j] = if i > 0 { up[i - 1][j] + 1 } else { 1 };
            }
        }
    }
    let mut best: i64 = 0;
    for i in 0..rows {
        for j in 0..cols {
            let mut k = left[i][j].min(up[i][j]);
            while k > best {
                let ku = k as usize;
                if left[i + 1 - ku][j] >= k && up[i][j + 1 - ku] >= k {
                    best = k;
                }
                k -= 1;
            }
        }
    }
    best * best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1139;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..20 {
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..100 {
            let row: Vec<i64> = (0..100).map(|_| if next_random(&mut seed) % 100 < 95 { 1 } else { 0 }).collect();
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..300 {
        for g in 0..20 {
            let i = (next_random(&mut seed) % 100) as usize;
            let j = (next_random(&mut seed) % 100) as usize;
            grids[g][i][j] = 1 - grids[g][i][j];
            let area = largest1_bordered_square(&grids[g]);
            total += area;
            check = (check * 131 + area + 1) % 1000000007;
        }
    }
    println!("300 rounds over 20 grids of 100 by 100: areas total {}, checksum {}", total, check);
}
