// Benchmark for #378: mirror of kth_smallest.kara.

fn count_at_most(matrix: &[Vec<i64>], x: i64) -> i64 {
    let n = matrix.len() as i64;
    let mut count = 0;
    let mut row = n - 1;
    let mut col = 0;
    while row >= 0 && col < n {
        if matrix[row as usize][col as usize] <= x {
            count += row + 1;
            col += 1;
        } else {
            row -= 1;
        }
    }
    count
}

fn kth_smallest(matrix: &[Vec<i64>], k: i64) -> i64 {
    let n = matrix.len();
    let mut lo = matrix[0][0];
    let mut hi = matrix[n - 1][n - 1];
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if count_at_most(matrix, mid) >= k {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    let n: i64 = 300;
    let mut seed: i64 = 378;
    let mut checksum: i64 = 0;
    for _ in 0..10 {
        let mut matrix: Vec<Vec<i64>> = Vec::new();
        for i in 0..n as usize {
            let mut row: Vec<i64> = Vec::new();
            for j in 0..n as usize {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                let d = (seed / 65536) % 10000;
                let v = if i == 0 && j == 0 {
                    -1000000000
                } else if i == 0 {
                    row[j - 1] + d
                } else if j == 0 {
                    matrix[i - 1][0] + d
                } else {
                    matrix[i - 1][j].max(row[j - 1]) + d
                };
                row.push(v);
            }
            matrix.push(row);
        }
        for _ in 0..10000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let k = 1 + (seed / 65536) % (n * n);
            checksum = (checksum * 1009 + kth_smallest(&matrix, k) + 1000000000) % 1000000007;
        }
    }
    println!("checksum {}", checksum);
}
