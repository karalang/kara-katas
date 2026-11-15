// LeetCode #1582 bench: the same row and column sums by iterators, in Rust.

fn num_special(mat: &[Vec<i64>]) -> i64 {
    let n = mat[0].len();
    let rows: Vec<i64> = mat.iter().map(|row| row.iter().sum()).collect();
    let cols: Vec<i64> = (0..n).map(|j| mat.iter().map(|row| row[j]).sum()).collect();
    mat.iter()
        .enumerate()
        .map(|(i, row)| (0..n).filter(|&j| row[j] == 1 && rows[i] == 1 && cols[j] == 1).count() as i64)
        .sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1582i64;
    let mut mats: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..2000 {
        let mat: Vec<Vec<i64>> = (0..100)
            .map(|_| (0..100).map(|_| if next_random(&mut seed) % 100 == 0 { 1 } else { 0 }).collect())
            .collect();
        mats.push(mat);
    }
    let (mut check, mut total) = (0i64, 0i64);
    for mat in mats.iter() {
        let special = num_special(mat);
        total += special;
        check = mix(check, special);
    }
    println!("2000 matrices of 100 x 100: special positions {}, checksum {}", total, check);
}
