// LeetCode #1572: Matrix Diagonal Sum -- bench: the ★ arm (two cells a
// row, the centre taken off once) over one matrix of 1001 rows of values
// from 1 to 100, built once; then 200000 rounds, each writing one random
// cell and summing the diagonals again.

fn diagonal_sum(mat: &[Vec<i64>]) -> i64 {
    let n = mat.len();
    let mut total = 0;
    for i in 0..n {
        total += mat[i][i] + mat[i][n - 1 - i];
    }
    if n % 2 == 1 {
        total -= mat[n / 2][n / 2];
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n: i64 = 1001;
    let rounds = 200000;
    let mut seed = 1572;
    let mut mat: Vec<Vec<i64>> = (0..n).map(|_| (0..n).map(|_| next_random(&mut seed) % 100 + 1).collect()).collect();
    let (mut check, mut total) = (0i64, 0i64);
    for _ in 0..rounds {
        let r = (next_random(&mut seed) % n) as usize;
        let c = (next_random(&mut seed) % n) as usize;
        mat[r][c] = next_random(&mut seed) % 100 + 1;
        let sum = diagonal_sum(&mat);
        total += sum;
        check = mix(check, sum);
    }
    println!("{} rounds on {} rows: sums total {}, checksum {}", rounds, n, total, check);
}
