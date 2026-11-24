// LeetCode #1329 bench, Rust mirror of the Kāra bench: the ★ arm (each
// diagonal read into a `Vec`, sorted and written back) on 8 matrices of 300
// by 300, values 1 to 100, built once. Then 100 passes, each setting one
// cell of every matrix from the checksum so far, answering it and folding
// two of the answer's cells plus the pass into the checksum.

fn sort_from(out: &mut Vec<Vec<i32>>, i0: usize, j0: usize) {
    let m = out.len();
    let n = out[0].len();
    let mut vals: Vec<i32> = Vec::new();
    let mut k = 0;
    while i0 + k < m && j0 + k < n {
        vals.push(out[i0 + k][j0 + k]);
        k += 1;
    }
    vals.sort();
    for (k, v) in vals.iter().enumerate() {
        out[i0 + k][j0 + k] = *v;
    }
}

fn diagonal_sort(mat: &Vec<Vec<i32>>) -> Vec<Vec<i32>> {
    let mut out = mat.clone();
    for i in 0..mat.len() {
        sort_from(&mut out, i, 0);
    }
    for j in 1..mat[0].len() {
        sort_from(&mut out, 0, j);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let size: usize = 300;
    let mut seed: i64 = 1329;
    let mut mats: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..8 {
        let mut mat: Vec<Vec<i32>> = Vec::new();
        for _ in 0..size {
            let mut row: Vec<i32> = Vec::new();
            for _ in 0..size {
                row.push((1 + next_random(&mut seed) % 100) as i32);
            }
            mat.push(row);
        }
        mats.push(mat);
    }
    let mut check: i64 = 0;
    for pass in 0..100 {
        for t in 0..8 {
            let r = (check % size as i64) as usize;
            let c = ((check / 7) % size as i64) as usize;
            mats[t][r][c] = (1 + (check / 13) % 100) as i32;
            let out = diagonal_sort(&mats[t]);
            check = (check * 31 + out[r][c] as i64 + out[size - 1][size / 2] as i64 + pass) % 1000000007;
        }
    }
    println!("100 passes over 8 matrices of 300 by 300: checksum {check}");
}
