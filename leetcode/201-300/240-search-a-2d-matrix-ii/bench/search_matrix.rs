// Benchmark harness for LeetCode #240 — Search a 2D Matrix II.
// Mirrors search_matrix.kara algorithm-for-algorithm.

fn search_matrix(flat: &[i64], rows: i64, cols: i64, target: i64) -> bool {
    if rows == 0 || cols == 0 {
        return false;
    }
    let mut r: i64 = 0;
    let mut c: i64 = cols - 1;
    while r < rows && c >= 0 {
        let v = flat[(r * cols + c) as usize];
        if v == target {
            return true;
        } else if v > target {
            c -= 1;
        } else {
            r += 1;
        }
    }
    false
}

fn main() {
    let rows: i64 = 1000;
    let cols: i64 = 1000;
    let iters: i64 = 120000;

    let mut flat: Vec<i64> = Vec::new();
    for r in 0..rows {
        for c in 0..cols {
            flat.push(r * 3 + c * 5);
        }
    }
    let maxv = (rows - 1) * 3 + (cols - 1) * 5;

    let mut sink: i64 = 0;
    let mut x: i64 = 12345;
    for it in 0..iters {
        x = (x * 1103515245 + 12345) % 2147483648;
        let target = (x / 65536) % (maxv + 2);
        if search_matrix(&flat, rows, cols, target) {
            sink = (sink + it + 1) % 1000000007;
        }
    }
    println!("{}", sink);
}
