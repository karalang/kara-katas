// Bench mirror of nqueens_bench.kara — bitmask solution-counting backtracker,
// weighted-checksum i64 sink, swept over n = 8..=13. rustc -O.
// See ../README.md § Benchmarks.

fn count(n: i64, row: i64, cols: i64, diag1: i64, diag2: i64, partial: i64, acc: &mut i64, sink: &mut i64) {
    if row == n {
        *acc += 1;
        *sink += partial;
        return;
    }
    let mut c = 0i64;
    while c < n {
        let bit_c = 1i64 << c;
        let bit_d1 = 1i64 << (row + c);
        let bit_d2 = 1i64 << (row - c + (n - 1));
        if (cols & bit_c) == 0 && (diag1 & bit_d1) == 0 && (diag2 & bit_d2) == 0 {
            count(n, row + 1, cols | bit_c, diag1 | bit_d1, diag2 | bit_d2, partial + c * (row + 1), acc, sink);
        }
        c += 1;
    }
}

fn main() {
    let n_lo: i64 = 8;
    let n_hi: i64 = 13;
    let mut total: i64 = 0;
    for n in n_lo..=n_hi {
        let mut acc: i64 = 0;
        let mut sink: i64 = 0;
        count(n, 0, 0, 0, 0, 0, &mut acc, &mut sink);
        total += acc * 100003 + sink;
    }
    println!("{}", total);
}
