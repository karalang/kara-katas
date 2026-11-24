// LeetCode #1292 bench: the ★ arm over 20 matrices of 300 by 300 with values
// up to 100, built once; then 100 passes, each setting one cell of every
// matrix and its threshold from the checksum so far and answering it.

fn max_side_length(mat: &[Vec<i64>], threshold: i64) -> i64 {
    let m = mat.len();
    let n = mat[0].len();
    let mut sum = vec![vec![0i64; n + 1]; m + 1];
    let mut best = 0usize;
    for i in 1..m + 1 {
        for j in 1..n + 1 {
            sum[i][j] = mat[i - 1][j - 1] + sum[i - 1][j] + sum[i][j - 1] - sum[i - 1][j - 1];
            let k = best + 1;
            if i >= k && j >= k && sum[i][j] - sum[i - k][j] - sum[i][j - k] + sum[i - k][j - k] <= threshold {
                best = k;
            }
        }
    }
    best as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1292;
    let mut mats: Vec<Vec<Vec<i64>>> = (0..20)
        .map(|_| (0..300).map(|_| (0..300).map(|_| next_random(&mut seed) % 101).collect()).collect())
        .collect();
    let mut check: i64 = 0;
    for p in 0..100 {
        for a in 0..mats.len() {
            mats[a][(check % 300) as usize][((check / 300) % 300) as usize] = check % 101;
            let threshold = check % 100001;
            check = (check * 31 + max_side_length(&mats[a], threshold) + p) % 1000000007;
        }
    }
    println!("100 passes over 20 matrices of 300 by 300: checksum {}", check);
}
