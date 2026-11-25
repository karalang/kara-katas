// LeetCode #1380 bench -- Rust: the ★ arm: each row's least value and
// each column's greatest found in one pass, then every cell that is both.

fn lucky_numbers(matrix: &[Vec<i32>]) -> Vec<i32> {
    let m = matrix.len();
    let n = matrix[0].len();
    let mut row_min = vec![i32::MAX; m];
    let mut col_max = vec![i32::MIN; n];
    for i in 0..m {
        for j in 0..n {
            row_min[i] = row_min[i].min(matrix[i][j]);
            col_max[j] = col_max[j].max(matrix[i][j]);
        }
    }
    let mut lucky: Vec<i32> = Vec::new();
    for i in 0..m {
        for j in 0..n {
            if matrix[i][j] == row_min[i] && matrix[i][j] == col_max[j] {
                lucky.push(matrix[i][j]);
            }
        }
    }
    lucky
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 matrices of 50 by 50 built once; then 20000 rounds, each swapping
    // two cells of one matrix and finding its lucky numbers (see the Kāra
    // bench)
    let n = 50i64;
    let mut seed = 1380i64;
    let mut grids: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..20 {
        let mut grid: Vec<Vec<i32>> = (0..n).map(|i| (0..n).map(|j| (i * n + j + 1) as i32).collect()).collect();
        for _ in 0..300 {
            let a = next_random(&mut seed) % (n * n);
            let b = next_random(&mut seed) % (n * n);
            let t = grid[(a / n) as usize][(a % n) as usize];
            grid[(a / n) as usize][(a % n) as usize] = grid[(b / n) as usize][(b % n) as usize];
            grid[(b / n) as usize][(b % n) as usize] = t;
        }
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for r in 0..20000i64 {
        let grid = &mut grids[(check % 20) as usize];
        let a = (check / 20) % (n * n);
        let b = (check / 7 + r) % (n * n);
        let t = grid[(a / n) as usize][(a % n) as usize];
        grid[(a / n) as usize][(a % n) as usize] = grid[(b / n) as usize][(b % n) as usize];
        grid[(b / n) as usize][(b % n) as usize] = t;
        let lucky = lucky_numbers(&grids[(check % 20) as usize]);
        let mut got = lucky.len() as i64;
        for &v in &lucky {
            got = got * 2503 + v as i64;
        }
        check = (check * 31 + got + r) % 1000000007;
    }
    println!("20000 rounds over 20 matrices of 50 by 50: checksum {check}");
}
