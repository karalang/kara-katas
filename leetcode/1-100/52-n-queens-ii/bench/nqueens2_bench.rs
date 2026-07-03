// Bench mirror of nqueens2_bench.kara — return-value counting backtracker,
// weighted-checksum i64 sink, swept over n = 9..=13. rustc -O.
// See ../README.md § Benchmarks.

fn search(n: i64, row: i64, cols: i64, diag1: i64, diag2: i64, partial: i64) -> i64 {
    if row == n {
        return 1 + partial;
    }
    let mut acc = 0i64;
    let mut c = 0i64;
    while c < n {
        let bit_c = 1i64 << c;
        let bit_d1 = 1i64 << (row + c);
        let bit_d2 = 1i64 << (row - c + (n - 1));
        if (cols & bit_c) == 0 && (diag1 & bit_d1) == 0 && (diag2 & bit_d2) == 0 {
            acc += search(n, row + 1, cols | bit_c, diag1 | bit_d1, diag2 | bit_d2, partial + c * (row + 1));
        }
        c += 1;
    }
    acc
}

fn main() {
    let n_lo: i64 = 9;
    let n_hi: i64 = 13;
    let mut total: i64 = 0;
    for n in n_lo..=n_hi {
        total += search(n, 0, 0, 0, 0, 0);
    }
    println!("{}", total);
}
