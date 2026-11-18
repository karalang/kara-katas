// LeetCode #1611: Minimum One Bit Operations to Make Integers Zero -- the
// bench in Rust, mirroring one_bit.kara: n turned back from Gray code, the
// XOR of n and all its right shifts.

fn minimum_one_bit_operations(mut n: i32) -> i32 {
    let mut k = 0;
    while n > 0 {
        k ^= n;
        n >>= 1;
    }
    k
}

fn main() {
    let mut seed: i64 = 1611;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let numbers: Vec<i32> = (0..10000000)
        .map(|_| {
            let a = next_random();
            let b = next_random();
            ((a * 32768 + b) % 1000000001) as i32
        })
        .collect();
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for &n in &numbers {
        let ops = minimum_one_bit_operations(n) as i64;
        check = (check * 31 + ops + 1) % 1000000007;
        total += ops;
    }
    println!("10000000 numbers up to 10^9: total {total}, checksum {check}");
}
