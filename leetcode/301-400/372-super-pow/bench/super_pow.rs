// Benchmark for #372 -- mirror of super_pow.kara.

const MODULUS: i64 = 1337;

fn pow_mod(base: i64, exp: i64) -> i64 {
    let mut out = 1;
    for _ in 0..exp {
        out = out * base % MODULUS;
    }
    out
}

fn super_pow(a: i64, b: &[i64]) -> i64 {
    let base = a % MODULUS;
    let mut out = 1;
    for &d in b {
        out = pow_mod(out, 10) * pow_mod(base, d) % MODULUS;
    }
    out
}

fn main() {
    let mut seed: i64 = 372;
    let mut checksum: i64 = 0;
    let mut b = vec![0i64; 2000];
    for _ in 0..500 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let a = 1 + (high * 65536 + seed / 32768) % 2147483647;
        for k in 0..2000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let d = (seed / 65536) % 10;
            b[k] = if k == 0 && d == 0 { 1 } else { d };
        }
        checksum = (checksum * 1337 + super_pow(a, &b)) % 1000000007;
    }
    println!("checksum {}", checksum);
}
