// LeetCode #693: Binary Number with Alternating Bits -- bench program, Rust mirror of the ★ arm.

fn has_alternating_bits(n: i64) -> bool {
    let x = n ^ (n >> 1);
    x & (x + 1) == 0
}

fn main() {
    let mut seed: i64 = 693;
    let count: i64 = 100000000;
    let mut yes: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..count {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let n = (1431655765i64 >> (seed % 31)) ^ ((seed >> 8) % 4);
        if n > 0 && has_alternating_bits(n) {
            yes += 1;
            checksum = (checksum * 31 + n) % 1000000007;
        }
    }
    println!("{} numbers: {} alternate, checksum {}", count, yes, checksum);
}
