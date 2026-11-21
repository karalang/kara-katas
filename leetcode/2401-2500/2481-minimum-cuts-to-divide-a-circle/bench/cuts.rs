// LeetCode #2481: Minimum Cuts to Divide a Circle -- bench, Rust mirror
// of cuts.kara.

fn number_of_cuts(n: i64) -> i64 {
    if n == 1 {
        0
    } else if n % 2 == 0 {
        n / 2
    } else {
        n
    }
}

fn main() {
    let mut check: i64 = 0;
    for p in 0..500000 {
        let start = check % 100;
        for i in 0..100 {
            let n = 1 + (start + i) % 100;
            check = (check * 31 + number_of_cuts(n) + p) % 1000000007;
        }
    }
    println!("500000 passes over every count from 1 to 100: checksum {}", check);
}
