// LeetCode #1492: The kth Factor of n -- the bench in Rust, mirroring
// kth_factor.kara: every i from 1 to n tried in order.

fn kth_factor(n: i32, k: i32) -> i32 {
    let mut left = k;
    for i in 1..=n {
        if n % i == 0 {
            left -= 1;
            if left == 0 {
                return i;
            }
        }
    }
    -1
}

fn main() {
    let mut check: i64 = 0;
    for pass in 0..400i64 {
        for n in 1..=1000i64 {
            let k = (1 + (n + pass + check) % 40) as i32;
            check = (check * 31 + kth_factor(n as i32, k) as i64 + 2) % 1000000007;
        }
    }
    println!("400 passes over n up to 1000: checksum {}", check);
}
