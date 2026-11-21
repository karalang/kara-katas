// LeetCode #2485: Find the Pivot Integer -- bench, Rust mirror of
// pivot.kara.

fn pivot_integer(n: i64) -> i64 {
    let total = n * (n + 1) / 2;
    let x = (total as f64).sqrt().round() as i64;
    if x * x == total {
        x
    } else {
        -1
    }
}

fn main() {
    let mut check: i64 = 0;
    for p in 0..24000 {
        let start = check % 1000;
        for i in 0..1000 {
            let n = 1 + (start + i) % 1000;
            check = (check * 31 + pivot_integer(n) + 2 + p) % 1000000007;
        }
    }
    println!("24000 passes over every count from 1 to 1000: checksum {}", check);
}
