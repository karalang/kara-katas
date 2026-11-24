// LeetCode #1337 bench, Rust mirror of the Kāra bench: the ★ arm on 50
// matrices of 100 by 100 built once, then 2000 passes, each rewriting one
// row of every matrix and choosing k from the checksum so far, answering
// every matrix.

fn soldiers(row: &[i32]) -> usize {
    let mut low = 0;
    let mut high = row.len();
    while low < high {
        let mid = (low + high) / 2;
        if row[mid] == 1 {
            low = mid + 1;
        } else {
            high = mid;
        }
    }
    low
}

fn k_weakest_rows(mat: &[Vec<i32>], k: i32) -> Vec<i32> {
    let mut rows: Vec<(usize, usize)> = Vec::new();
    for (i, row) in mat.iter().enumerate() {
        rows.push((soldiers(row), i));
    }
    rows.sort();
    rows.iter().take(k as usize).map(|p| p.1 as i32).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 100i64;
    let mut seed = 1337i64;
    let mut mats: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..50 {
        let mut mat: Vec<Vec<i32>> = Vec::new();
        for _ in 0..n {
            let s = next_random(&mut seed) % (n + 1);
            let mut row = vec![0i32; n as usize];
            for c in 0..s as usize {
                row[c] = 1;
            }
            mat.push(row);
        }
        mats.push(mat);
    }
    let mut check: i64 = 0;
    for pass in 0..2000i64 {
        let k = (1 + check % n) as i32;
        for t in 0..50 {
            let r = (check % n) as usize;
            let s = check / 7 % (n + 1);
            for c in 0..n {
                mats[t][r][c as usize] = if c < s { 1 } else { 0 };
            }
            let rows = k_weakest_rows(&mats[t], k);
            check = (check * 31 + rows[0] as i64 + rows[rows.len() - 1] as i64 + pass) % 1000000007;
        }
    }
    println!("2000 passes over 50 matrices of 100 by 100: checksum {}", check);
}
