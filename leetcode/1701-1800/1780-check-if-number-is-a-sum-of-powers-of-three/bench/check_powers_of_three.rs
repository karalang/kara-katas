// LeetCode #1780: Check if Number is a Sum of Powers of Three -- the bench in
// Rust, mirroring check_powers_of_three.kara: base-3 digits read off from the
// lowest, on every n from 1 to 10^7, five rounds over.

fn check_powers_of_three(n: i32) -> bool {
    let mut rest = n;
    while rest > 0 {
        if rest % 3 == 2 {
            return false;
        }
        rest /= 3;
    }
    true
}

fn main() {
    let mut count: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..5i64 {
        for n in 1..10000001i32 {
            if check_powers_of_three(n) {
                count += 1;
                check = (check * 31 + n as i64 + round) % 1000000007;
            }
        }
    }
    println!("5 rounds of 1 to 10000000: {} sums, checksum {}", count, check);
}
