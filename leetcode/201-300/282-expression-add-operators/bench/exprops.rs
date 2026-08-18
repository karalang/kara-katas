// LeetCode 282 bench mirror — Rust. Same search, same string building.
const INPUTS: usize = 220;
const NDIG: usize = 9;
struct S { num: Vec<u8>, target: i64, found: i64, hash: i64 }
fn search(s: &mut S, pos: usize, expr: &str, cur: i64, last: i64) {
    if pos == NDIG {
        if cur == s.target { s.found += 1; s.hash = (s.hash * 31 + expr.len() as i64) % 1000000007; }
        return;
    }
    for end in pos + 1..=NDIG {
        if end > pos + 1 && s.num[pos] == b'0' { return; }
        let mut n: i64 = 0;
        for k in pos..end { n = n * 10 + (s.num[k] - b'0') as i64; }
        let piece = String::from_utf8(s.num[pos..end].to_vec()).unwrap();
        if pos == 0 {
            search(s, end, &piece, n, n);
        } else {
            search(s, end, &format!("{}+{}", expr, piece), cur + n, n);
            search(s, end, &format!("{}-{}", expr, piece), cur - n, -n);
            search(s, end, &format!("{}*{}", expr, piece), cur - last + last * n, last * n);
        }
    }
}
fn main() {
    let mut seed: i64 = 20260820;
    let mut s = S { num: vec![0u8; NDIG], target: 0, found: 0, hash: 0 };
    let mut total = 0i64;
    for _ in 0..INPUTS {
        for d in 0..NDIG {
            seed = (seed*1103515245+12345)%2147483648;
            s.num[d] = b'0' + 1 + ((seed/19) % 6) as u8;
        }
        seed = (seed*1103515245+12345)%2147483648;
        s.target = (seed/23) % 40;
        s.found = 0;
        search(&mut s, 0, "", 0, 0);
        total += s.found;
    }
    println!("{} {}", total, s.hash);
}
