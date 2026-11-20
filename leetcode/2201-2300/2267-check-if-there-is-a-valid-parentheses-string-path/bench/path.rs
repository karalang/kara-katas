// LeetCode #2267: Check if There Is a Valid Parentheses String Path --
// Rust mirror of the ★ arm (path.kara): a table reach[i][j][b] of the
// balances some path to (i, j) can end with, as nested `Vec`s. Output is
// byte-identical to path.kara.

fn has_valid_path(grid: &[Vec<char>]) -> bool {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    if (m + n - 1) % 2 == 1 || grid[0][0] == ')' || grid[(m - 1) as usize][(n - 1) as usize] == '(' {
        return false;
    }
    let most = (m + n) / 2 + 1;
    let mut reach = vec![vec![vec![false; (most + 1) as usize]; n as usize]; m as usize];
    reach[0][0][1] = true;
    for i in 0..m as usize {
        for j in 0..n as usize {
            if i == 0 && j == 0 {
                continue;
            }
            let step = if grid[i][j] == '(' { 1 } else { -1 };
            for b in 0..most + 1 {
                let from = b - step;
                if from < 0 || from > most {
                    continue;
                }
                let f = from as usize;
                if (i > 0 && reach[i - 1][j][f]) || (j > 0 && reach[i][j - 1][f]) {
                    reach[i][j][b as usize] = true;
                }
            }
        }
    }
    reach[(m - 1) as usize][(n - 1) as usize][0]
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2267;
    let mut found = 0;
    let mut check: i64 = 0;
    for t in 0..20 {
        let open = 50 + t;
        let mut grid: Vec<Vec<char>> = (0..100)
            .map(|_| (0..99).map(|_| if next_random(&mut seed) % 100 < open { '(' } else { ')' }).collect())
            .collect();
        grid[0][0] = '(';
        grid[99][98] = ')';
        let valid = has_valid_path(&grid);
        if valid {
            found += 1;
        }
        check = (check * 31 + if valid { 2 } else { 1 }) % 1000000007;
    }
    println!("20 grids of 100 by 99: {found} with a path, checksum {check}");
}
