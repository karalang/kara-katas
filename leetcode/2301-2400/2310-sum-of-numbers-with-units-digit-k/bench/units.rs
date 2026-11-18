// LeetCode #2310: Sum of Numbers With Units Digit K -- the bench, the ★
// arm in Rust. The least count from 1 to 10 whose multiple of `k` fits
// within `num` and leaves a multiple of 10.

fn minimum_numbers(num: i64, k: i64) -> i64 {
    if num == 0 {
        return 0;
    }
    for n in 1..=10 {
        if n * k <= num && (num - n * k) % 10 == 0 {
            return n;
        }
    }
    -1
}

fn main() {
    let mut check: i64 = 0;
    for p in 0..300 {
        for num in 0..=3000 {
            for k in 0..10 {
                check = (check * 31 + minimum_numbers(num, k) + 1 + p) % 1000000007;
            }
        }
    }
    println!("300 passes over 3001 sums and 10 digits: checksum {}", check);
}
