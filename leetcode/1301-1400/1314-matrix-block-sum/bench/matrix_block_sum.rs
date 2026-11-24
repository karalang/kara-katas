// LeetCode #1314 bench, Rust: the ★ arm (a table of sums over every
// top-left rectangle, each block's sum four lookups) on the same 20
// matrices and 200 passes.

fn matrix_block_sum(mat: &[Vec<i64>], k: i64) -> Vec<Vec<i64>> {
    let m = mat.len() as i64;
    let n = mat[0].len() as i64;
    let mut sums = vec![vec![0i64; n as usize + 1]; m as usize + 1];
    for i in 0..m as usize {
        for j in 0..n as usize {
            sums[i + 1][j + 1] = mat[i][j] + sums[i][j + 1] + sums[i + 1][j] - sums[i][j];
        }
    }
    let mut out = vec![vec![0i64; n as usize]; m as usize];
    for i in 0..m {
        let top = (i - k).max(0) as usize;
        let bottom = (i + k + 1).min(m) as usize;
        for j in 0..n {
            let left = (j - k).max(0) as usize;
            let right = (j + k + 1).min(n) as usize;
            out[i as usize][j as usize] = sums[bottom][right] - sums[top][right] - sums[bottom][left] + sums[top][left];
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 100;
    let mut seed = 1314;
    let mut mats: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..20 {
        let mut mat = Vec::new();
        for _ in 0..n {
            let mut row = Vec::new();
            for _ in 0..n {
                row.push(1 + next_random(&mut seed) % 100);
            }
            mat.push(row);
        }
        mats.push(mat);
    }
    let mut check: i64 = 0;
    for pass in 0..200 {
        for g in 0..20 {
            mats[g][(check % n) as usize][((check / 7) % n) as usize] = 1 + (check / 11) % 100;
            let k = if check % 4 == 0 { 1 + (check / 13) % 100 } else { 1 + (check / 13) % 5 };
            let got = matrix_block_sum(&mats[g], k);
            check = (check * 31 + got[((check / 3) % n) as usize][((check / 17) % n) as usize]) % 1000000007;
            check = (check * 31 + got[((check / 19) % n) as usize][((check / 23) % n) as usize] + pass) % 1000000007;
        }
    }
    println!("200 passes over 20 matrices of 100 by 100: checksum {}", check);
}
