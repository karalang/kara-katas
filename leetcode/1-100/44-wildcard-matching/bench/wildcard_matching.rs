// LeetCode #44 bench mirror — Rust, the greedy two-pointer matcher (★).
//
// Mirrors bench/wildcard_matching.kara exactly: one cursor in each of s and p, with
// star/matched scalars for O(1) backtracking. Build s and a multi-star pattern p once, punch
// one s slot per iteration, fold the boolean into a rolling checksum. Same workload + sink as
// every other mirror.

fn is_match(s: &[u8], p: &[u8]) -> bool {
    let n = s.len() as i64;
    let m = p.len() as i64;
    let mut i = 0i64;
    let mut j = 0i64;
    let mut star = -1i64;
    let mut matched = 0i64;
    while i < n {
        if j < m && (p[j as usize] == b'?' || p[j as usize] == s[i as usize]) {
            i += 1;
            j += 1;
        } else if j < m && p[j as usize] == b'*' {
            star = j;
            matched = i;
            j += 1;
        } else if star != -1 {
            matched += 1;
            i = matched;
            j = star + 1;
        } else {
            return false;
        }
    }
    while j < m && p[j as usize] == b'*' {
        j += 1;
    }
    j == m
}

fn main() {
    let total: i64 = 300000;
    let modulus: i64 = 1000000007;
    let n: i64 = 240;

    let mut s: Vec<u8> = (0..n).map(|a| b'a' + (a % 3) as u8).collect();
    let mut p: Vec<u8> = Vec::new();
    for _ in 0..8 {
        p.push(b'*');
        p.push(b'a');
        p.push(b'b');
        p.push(b'c');
    }
    p.push(b'*');

    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        s[(k % n) as usize] = b'a' + (k % 4) as u8;
        let bit = if is_match(&s, &p) { 1 } else { 0 };
        acc = (acc * 131 + bit) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
