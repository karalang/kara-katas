// Benchmark workload for LeetCode #343 — Rust mirror of integer_break.kara.

const LEN: i64 = 20000;
const PUNCHES: i64 = 20;
const MODULUS: i64 = 1073741789;

fn integer_break(n: i64) -> i64 {
    let mut best: Vec<i64> = vec![0; (n + 1) as usize];
    for i in 2..n + 1 {
        for j in 1..i {
            let whole = j * (i - j);
            let broken = j * best[(i - j) as usize];
            if whole > best[i as usize] {
                best[i as usize] = whole;
            }
            if broken > best[i as usize] {
                best[i as usize] = broken;
            }
        }
    }
    best[n as usize]
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 343;
    let mut a: Vec<i64> = Vec::new();
    for _ in 0..LEN {
        a.push(2 + next(&mut seed) % 57);
    }
    let mut sink: i64 = 0;
    for _ in 0..PUNCHES {
        let pos = (next(&mut seed) * 32768 + next(&mut seed)) % LEN;
        a[pos as usize] = 2 + next(&mut seed) % 57;
        let mut sum: i64 = 0;
        for &n in &a {
            sum = (sum + integer_break(n)) % MODULUS;
        }
        sink = (sink * 31 + sum) % MODULUS;
    }
    println!("sink {}", sink);
}
