// LeetCode #2160: Minimum Sum of Four Digit Number After Splitting Digits
// -- the benchmark's Rust mirror of digits.kara.

fn minimum_sum(num: i64) -> i64 {
    let mut d: Vec<i64> = num.to_string().chars().map(|c| c.to_digit(10).unwrap() as i64).collect();
    d.sort();
    (d[0] * 10 + d[2]) + (d[1] * 10 + d[3])
}

fn main() {
    let mut total = 0i64;
    let mut check = 0i64;
    for pass in 0..200i64 {
        for k in 0..9000i64 {
            let num = 1000 + (k + 37 * pass) % 9000;
            let sum = minimum_sum(num);
            total += sum;
            check = (check * 31 + sum + pass) % 1000000007;
        }
    }
    println!("1800000 solves: {} in all, checksum {}", total, check);
}
