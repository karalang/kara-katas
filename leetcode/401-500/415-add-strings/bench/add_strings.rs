// LeetCode #415 bench — Rust (mirror of add_strings.kara).
//
// Two-pointer column add + digit-table render, building one growing `String`
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

fn add_strings(a: &str, b: &str) -> String {
    let ab = a.as_bytes();
    let bb = b.as_bytes();
    let mut i = ab.len() as i64 - 1;
    let mut j = bb.len() as i64 - 1;
    let mut carry = 0i64;
    let mut buf: Vec<usize> = Vec::new();
    while i >= 0 || j >= 0 || carry > 0 {
        let mut sum = carry;
        if i >= 0 {
            sum += (ab[i as usize] - b'0') as i64;
            i -= 1;
        }
        if j >= 0 {
            sum += (bb[j as usize] - b'0') as i64;
            j -= 1;
        }
        buf.push((sum % 10) as usize);
        carry = sum / 10;
    }
    let mut s = String::new();
    for &d in buf.iter().rev() {
        s.push(D[d] as char);
    }
    s
}

fn main() {
    let total: i64 = 500000;
    let a = "31415926535897932384626433832795028841";
    let mut out = String::new();
    for k in 0..total {
        let v = (k * 2654435761) & 0xffffffff;
        let b = digits_of(v);
        out.push_str(&add_strings(a, &b));
    }
    let sum: i64 = out.bytes().map(|x| x as i64).sum();
    println!("{}", sum);
}
