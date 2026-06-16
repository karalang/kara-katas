// LeetCode #13 — rayon-parallel Rust mirror (par lane, greedy).
// Same int_to_roman / roman_to_int as ../greedy.rs; the K=10M reduction runs
// across a rayon pool. Hand-tuned-parallel comparator for Kāra's auto-par.
// Sink matches the kara/rust/c/go mirrors.

fn int_to_roman(num: i64) -> Vec<char> {
    let mut out: Vec<char> = Vec::with_capacity(15);
    let mut n = num;
    while n >= 1000 { out.push('M'); n -= 1000; }
    if    n >= 900  { out.push('C'); out.push('M'); n -= 900; }
    if    n >= 500  { out.push('D'); n -= 500; }
    if    n >= 400  { out.push('C'); out.push('D'); n -= 400; }
    while n >= 100  { out.push('C'); n -= 100; }
    if    n >= 90   { out.push('X'); out.push('C'); n -= 90; }
    if    n >= 50   { out.push('L'); n -= 50; }
    if    n >= 40   { out.push('X'); out.push('L'); n -= 40; }
    while n >= 10   { out.push('X'); n -= 10; }
    if    n >= 9    { out.push('I'); out.push('X'); n -= 9; }
    if    n >= 5    { out.push('V'); n -= 5; }
    if    n >= 4    { out.push('I'); out.push('V'); n -= 4; }
    while n >= 1    { out.push('I'); n -= 1; }
    out
}

fn value(c: char) -> i64 {
    match c {
        'I' => 1,
        'V' => 5,
        'X' => 10,
        'L' => 50,
        'C' => 100,
        'D' => 500,
        'M' => 1000,
        _ => 0,
    }
}

fn roman_to_int(r: &Vec<char>) -> i64 {
    let n = r.len();
    let mut total: i64 = 0;
    let mut i: usize = 0;
    while i < n {
        let cur = value(r[i]);
        if i + 1 < n {
            let nxt = value(r[i + 1]);
            if cur < nxt {
                total -= cur;
            } else {
                total += cur;
            }
        } else {
            total += cur;
        }
        i += 1;
    }
    total
}

fn main() {
    use rayon::prelude::*;
    let k_iters: i64 = 10_000_000;
    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let raw: i64 = k.wrapping_mul(2_654_435_769).wrapping_add(305_419_896);
            let num: i64 = (raw % 3999 + 3999) % 3999 + 1;
            let r = int_to_roman(num);
            roman_to_int(&r)
        })
        .sum();
    println!("{}", sum);
}
