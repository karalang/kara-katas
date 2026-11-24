// LeetCode #1304 bench in Rust: the ★ arm (the pairs i and -i, and 0 when
// n is odd, pushed onto a fresh `Vec`), the same 10^6 calls.

fn sum_zero(n: i64) -> Vec<i64> {
    let mut out = Vec::new();
    for i in 1..n / 2 + 1 {
        out.push(i);
        out.push(-i);
    }
    if n % 2 == 1 {
        out.push(0);
    }
    out
}

fn main() {
    let mut check: i64 = 0;
    for call in 0..1000000i64 {
        let n = 1 + check % 1000;
        let got = sum_zero(n);
        let x = got[((check / 1000) % n) as usize];
        check = (check * 31 + x + 1000 + call) % 1000000007;
    }
    println!("1000000 calls: checksum {check}");
}
