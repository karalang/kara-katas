// Benchmark workload — half-reverse Palindrome Number. Rust mirror of
// bench/palindrome.kara. Same N, K, same LCG fill + every-16th
// manufactured 8-digit palindrome, same sink formula — see that file's
// header for the workload rationale.

fn is_palindrome(x: i32) -> bool {
    if x < 0 || (x % 10 == 0 && x != 0) {
        return false;
    }
    let mut x = x;
    let mut reversed: i32 = 0;
    while x > reversed {
        reversed = reversed * 10 + x % 10;
        x /= 10;
    }
    x == reversed || x == reversed / 10
}

fn manufacture_palindrome(v32: i32) -> i32 {
    let lo = if v32 < 0 { -v32 } else { v32 };
    let four_raw = lo % 10000;
    let four = if four_raw < 1000 { four_raw + 1000 } else { four_raw };
    let d0 = four % 10;
    let d1 = (four / 10) % 10;
    let d2 = (four / 100) % 10;
    let d3 = (four / 1000) % 10;
    let rev = d0 * 1000 + d1 * 100 + d2 * 10 + d3;
    four * 10000 + rev
}

fn main() {
    let n: i64 = 1024;
    let k_iters: i64 = 50_000_000;

    let mut inputs: Vec<i32> = Vec::with_capacity(n as usize);
    for i in 0..n {
        let raw: i64 = i.wrapping_mul(2_654_435_769).wrapping_add(305_419_896);
        let v32: i32 = raw as i32;
        if i % 16 == 0 {
            inputs.push(manufacture_palindrome(v32));
        } else {
            inputs.push(v32);
        }
    }

    let mut sum: i64 = 0;
    for k in 0..k_iters {
        let idx = (k % n) as usize;
        let x = inputs[idx];
        sum += if is_palindrome(x) { 1 } else { 0 };
    }
    println!("{}", sum);
}
