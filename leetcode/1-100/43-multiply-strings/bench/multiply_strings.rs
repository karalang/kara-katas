// LeetCode #43 bench — Rust (mirror of multiply_strings.kara).
//
// The digit-grid multiply + digit-table render, building one growing `String`
// (the apples-to-apples String-builder peer to Kāra), then byte-checksum it.
// `rustc -O` wraps on overflow; the bench also builds a `-C overflow-checks=on`
// variant to match Kāra's checked-by-default semantics.

const D: &[u8] = b"0123456789";

fn digits_of(n: i64) -> String {
    if n == 0 {
        return "0".to_string();
    }
    let mut v = n;
    let mut buf: Vec<usize> = Vec::new();
    while v > 0 {
        buf.push((v % 10) as usize);
        v /= 10;
    }
    let mut s = String::new();
    for &d in buf.iter().rev() {
        s.push(D[d] as char);
    }
    s
}

fn multiply(a: &str, b: &str) -> String {
    let ab = a.as_bytes();
    let bb = b.as_bytes();
    let m = ab.len();
    let n = bb.len();
    let mut res = vec![0i64; m + n];
    for i in (0..m).rev() {
        let d1 = (ab[i] - b'0') as i64;
        for j in (0..n).rev() {
            let d2 = (bb[j] - b'0') as i64;
            let lo = i + j + 1;
            let hi = i + j;
            let sum = d1 * d2 + res[lo];
            res[lo] = sum % 10;
            res[hi] += sum / 10;
        }
    }
    let mut k = 0;
    while k < res.len() && res[k] == 0 {
        k += 1;
    }
    let mut s = String::new();
    while k < res.len() {
        s.push(D[res[k] as usize] as char);
        k += 1;
    }
    if s.is_empty() {
        return "0".to_string();
    }
    s
}

fn main() {
    let total: i64 = 300000;
    let a = "31415926535897932384626433832795028841";
    let mut out = String::new();
    for k in 0..total {
        let v = (k * 2654435761) & 0xffffffff;
        let b = digits_of(v);
        out.push_str(&multiply(a, &b));
    }
    let sum: i64 = out.bytes().map(|x| x as i64).sum();
    println!("{}", sum);
}
