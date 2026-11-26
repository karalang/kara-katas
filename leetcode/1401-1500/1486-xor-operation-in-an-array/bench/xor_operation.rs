// LeetCode #1486: XOR Operation in an Array -- bench, the Rust twin of
// xor_operation.kara.

fn xor_operation(n: i32, start: i32) -> i32 {
    let mut x: i32 = 0;
    for i in 0..n {
        x ^= start + 2 * i;
    }
    x
}

fn main() {
    let mut check: i64 = 0;
    for q in 0..2000000i64 {
        let n = (1 + (check + q) % 1000) as i32;
        let start = ((check / 7 + q * 13) % 1001) as i32;
        check = (check * 31 + xor_operation(n, start) as i64) % 1000000007;
    }
    println!("2000000 calls: checksum {}", check);
}
