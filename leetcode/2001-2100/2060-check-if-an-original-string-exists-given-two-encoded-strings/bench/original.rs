// LeetCode #2060: Check if an Original String Exists Given Two Encoded
// Strings -- Rust mirror of the ★ arm's benchmark (original.kara): the same
// 2000 pairs, each answered by one search over (place, place, lead) with a
// set of the states tried.
use std::collections::HashSet;

fn search(a: &[u8], b: &[u8], i: usize, j: usize, lead: i64, seen: &mut HashSet<(usize, usize, i64)>) -> bool {
    if i == a.len() && j == b.len() {
        return lead == 0;
    }
    if !seen.insert((i, j, lead)) {
        return false;
    }
    if i < a.len() && a[i].is_ascii_digit() {
        let mut num = 0i64;
        let mut k = i;
        while k < a.len() && a[k].is_ascii_digit() {
            num = num * 10 + (a[k] - b'0') as i64;
            k += 1;
            if search(a, b, k, j, lead + num, seen) {
                return true;
            }
        }
        return false;
    }
    if j < b.len() && b[j].is_ascii_digit() {
        let mut num = 0i64;
        let mut k = j;
        while k < b.len() && b[k].is_ascii_digit() {
            num = num * 10 + (b[k] - b'0') as i64;
            k += 1;
            if search(a, b, i, k, lead - num, seen) {
                return true;
            }
        }
        return false;
    }
    if lead > 0 {
        return j < b.len() && search(a, b, i, j + 1, lead - 1, seen);
    }
    if lead < 0 {
        return i < a.len() && search(a, b, i + 1, j, lead + 1, seen);
    }
    i < a.len() && j < b.len() && a[i] == b[j] && search(a, b, i + 1, j + 1, 0, seen)
}

fn possibly_equals(s1: &[u8], s2: &[u8]) -> bool {
    let mut seen = HashSet::new();
    search(s1, s2, 0, 0, 0, &mut seen)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn dense(seed: &mut i64) -> Vec<u8> {
    let mut s = Vec::new();
    loop {
        let len = next_random(seed) % 3 + 1;
        let mut run = Vec::new();
        for _ in 0..len {
            run.push(b'1' + (next_random(seed) % 9) as u8);
        }
        let letter = if next_random(seed) % 2 == 0 { b'u' } else { b'v' };
        if s.len() + run.len() + 1 > 40 {
            return s;
        }
        s.extend_from_slice(&run);
        s.push(letter);
    }
}

fn main() {
    let mut seed = 2060i64;
    let mut possible = 0;
    let mut check = 0i64;
    for _ in 0..2000 {
        let s1 = dense(&mut seed);
        let s2 = dense(&mut seed);
        let ok = possibly_equals(&s1, &s2);
        if ok {
            possible += 1;
        }
        check = (check * 31 + if ok { 2 } else { 1 }) % 1000000007;
    }
    println!("2000 pairs: {} possible, checksum {}", possible, check);
}
