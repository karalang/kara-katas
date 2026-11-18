// LeetCode #1605: Find Valid Matrix Given Row and Column Sums -- the bench
// in Rust, mirroring restore.kara: greedy, cell by cell in reading order.

fn restore_matrix(row_sum: Vec<i32>, col_sum: Vec<i32>) -> Vec<Vec<i32>> {
    let mut rows = row_sum;
    let mut cols = col_sum;
    let mut m = Vec::new();
    for i in 0..rows.len() {
        let mut row = vec![0; cols.len()];
        for j in 0..cols.len() {
            let x = rows[i].min(cols[j]);
            row[j] = x;
            rows[i] -= x;
            cols[j] -= x;
        }
        m.push(row);
    }
    m
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1605;
    let mut problems = Vec::new();
    for _ in 0..100 {
        let mut row_sum = vec![0i32; 1000];
        let mut col_sum = vec![0i32; 1000];
        for i in 0..1000 {
            for j in 0..1000 {
                let x = (next_random(&mut seed) % 1001) as i32;
                row_sum[i] += x;
                col_sum[j] += x;
            }
        }
        problems.push((row_sum, col_sum));
    }
    let mut check = 0;
    let mut nonzero = 0;
    for (row_sum, col_sum) in problems.iter() {
        let m = restore_matrix(row_sum.clone(), col_sum.clone());
        for row in m.iter() {
            for x in row.iter() {
                if *x != 0 {
                    nonzero += 1;
                    check = mix(check, *x as i64);
                }
            }
        }
    }
    println!("100 problems of 1000 by 1000: {} cells not zero, checksum {}", nonzero, check);
}
