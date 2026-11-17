// LeetCode #2235: Add Two Integers -- the benchmark's Rust mirror of
// add.kara: 10^7 pairs drawn and added, folded into a checksum.

fn sum(num1: i64, num2: i64) -> i64 {
    num1 + num2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2235i64;
    let mut check = 0i64;
    for _ in 0..10000000 {
        let num1 = next_random(&mut seed) % 201 - 100;
        let num2 = next_random(&mut seed) % 201 - 100;
        check = (check * 31 + sum(num1, num2) + 200) % 1000000007;
    }
    println!("10^7 pairs: checksum {}", check);
}
