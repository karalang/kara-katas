// LeetCode 282 bench mirror — Rust. Same search, same per-branch allocation.
const INPUTS: i64 = 220;
const NDIG: usize = 9;

fn make_input(idx: i64) -> Vec<u8> {
    let mut seed = (20260820 + idx * 7919) % 2147483648;
    let mut v = vec![0u8; NDIG];
    for d in 0..NDIG {
        seed = (seed*1103515245+12345)%2147483648;
        v[d] = b'0' + 1 + ((seed/19) % 6) as u8;
    }
    v
}
fn target_for(idx: i64) -> i64 {
    let mut seed = (20260820 + idx * 7919) % 2147483648;
    for _ in 0..10 { seed = (seed*1103515245+12345)%2147483648; }
    (seed/23) % 40
}
fn search(num: &[u8], target: i64, pos: usize, expr: &str, cur: i64, last: i64,
          found: &mut i64, hash: &mut i64) {
    if pos == NDIG {
        if cur == target { *found += 1; *hash = (*hash * 31 + expr.len() as i64) % 1000000007; }
        return;
    }
    for end in pos + 1..=NDIG {
        if end > pos + 1 && num[pos] == b'0' { return; }
        let mut n: i64 = 0;
        for k in pos..end { n = n * 10 + (num[k] - b'0') as i64; }
        let piece = String::from_utf8(num[pos..end].to_vec()).unwrap();
        if pos == 0 {
            search(num, target, end, &piece, n, n, found, hash);
        } else {
            search(num, target, end, &format!("{}+{}", expr, piece), cur + n, n, found, hash);
            search(num, target, end, &format!("{}-{}", expr, piece), cur - n, -n, found, hash);
            search(num, target, end, &format!("{}*{}", expr, piece), cur - last + last*n, last*n, found, hash);
        }
    }
}
fn solve_one(i: i64) -> i64 {
    let num = make_input(i);
    let target = target_for(i);
    let (mut found, mut hash) = (0i64, 0i64);
    search(&num, target, 0, "", 0, 0, &mut found, &mut hash);
    (i * 1000003 + found * 31 + hash) % 1000000007
}
fn main() {
    let mut sink = 0i64;
    for i in 0..INPUTS { sink = (sink + solve_one(i)) % 1000000007; }
    println!("{}", sink);
}
