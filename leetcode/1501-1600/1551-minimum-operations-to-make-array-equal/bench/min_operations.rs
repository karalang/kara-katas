// LeetCode #1551: Minimum Operations to Make Array Equal -- bench: the ★
// arm (the lower half's distance from the mean, added up place by place)
// for every n from 1 to 10000, in 100 passes. Rust mirror of min_operations.kara.

fn min_operations(n: i64) -> i64 {
    let mut operations = 0;
    for i in 0..n / 2 {
        operations += n - (2 * i + 1);
    }
    operations
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut check = 0i64;
    for pass in 0..100i64 {
        for n in 1..=10000i64 {
            check = mix(check, min_operations(n) + pass);
        }
    }
    println!("100 passes over n from 1 to 10000: checksum {}", check);
}
