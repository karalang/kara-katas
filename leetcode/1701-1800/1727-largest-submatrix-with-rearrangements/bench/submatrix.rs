// LeetCode #1727: Largest Submatrix With Rearrangements -- the bench
// (submatrix.kara): each row's column heights sorted, the k-th from the
// shortest giving a submatrix n - k wide.

fn largest_submatrix(matrix: &[Vec<i32>]) -> i32 {
    let n = matrix[0].len();
    let mut heights = vec![0i32; n];
    let mut best = 0;
    for row in matrix.iter() {
        for j in 0..n {
            heights[j] = if row[j] == 1 { heights[j] + 1 } else { 0 };
        }
        let mut sorted = heights.clone();
        sorted.sort();
        for k in 0..n {
            best = best.max(sorted[k] * (n - k) as i32);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds: i64 = 50;
    let side = 316;
    let mut seed: i64 = 1727;
    let mut problems: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..count {
        let mut matrix: Vec<Vec<i32>> = Vec::new();
        for _ in 0..side {
            let row: Vec<i32> = (0..side)
                .map(|_| {
                    if next_random(&mut seed) % 8 == 0 {
                        0
                    } else {
                        1
                    }
                })
                .collect();
            matrix.push(row);
        }
        problems.push(matrix);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for matrix in problems.iter() {
            let answer = largest_submatrix(matrix) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!(
        "{} matrices of {} by {}, {} rounds: areas sum to {}, checksum {}",
        count, side, side, rounds, sum, check
    );
}
