// Benchmark for #660: base 9, read as base 10, as the Kara ★ arm.

fn new_integer(n: i64) -> i64 {
    let mut rest = n;
    let mut place = 1i64;
    let mut out = 0i64;
    while rest > 0 {
        out += rest % 9 * place;
        rest /= 9;
        place *= 10;
    }
    out
}

fn main() {
    let count = 50000000i64;
    let mut checksum: i64 = 0;
    for i in 0..count {
        let n = 1 + i * 16;
        checksum = (checksum * 31 + new_integer(n)) % 1000000007;
    }
    println!("{} values of n: checksum {}", count, checksum);
}
