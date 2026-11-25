// LeetCode #1351 bench -- Rust: a staircase walk from the bottom-left
// corner.

fn count_negatives(grid: &[Vec<i32>]) -> i32 {
    let n = grid[0].len();
    let mut row = grid.len() as i64 - 1;
    let mut col = 0;
    let mut count = 0;
    while row >= 0 && col < n {
        if grid[row as usize][col] < 0 {
            count += n - col;
            row -= 1;
        } else {
            col += 1;
        }
    }
    count as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1351;
    let mut grids: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..50 {
        let mut grid: Vec<Vec<i32>> = Vec::new();
        for i in 0..100 {
            let mut row: Vec<i32> = Vec::new();
            for j in 0..100 {
                let mut v: i32 = 60;
                if i > 0 {
                    v = v.min(grid[i - 1][j]);
                }
                if j > 0 {
                    v = v.min(row[j - 1]);
                }
                if i + j > 0 {
                    v -= (next_random(&mut seed) % 2) as i32;
                }
                row.push(v.max(-100));
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for r in 0..300000i64 {
        let k = (check % 50) as usize;
        let i = ((check / 50) % 100) as usize;
        let j = ((check / 5000) % 100) as usize;
        let g = &mut grids[k];
        let v = if check % 2 == 0 {
            let mut v: i32 = 100;
            if i > 0 {
                v = v.min(g[i - 1][j]);
            }
            if j > 0 {
                v = v.min(g[i][j - 1]);
            }
            v
        } else {
            let mut v: i32 = -100;
            if i < 99 {
                v = v.max(g[i + 1][j]);
            }
            if j < 99 {
                v = v.max(g[i][j + 1]);
            }
            v
        };
        g[i][j] = v;
        check = (check * 31 + count_negatives(&grids[k]) as i64 + r) % 1000000007;
    }
    println!("300000 rounds over 50 grids of 100 by 100: checksum {}", check);
}
