// LeetCode 756 — Pyramid Transition Matrix: benchmark, the ★ arm in Rust.
use std::collections::HashSet;

fn row_code(row: &[i64]) -> i64 {
    let mut code = 1;
    for x in row {
        code = code * 6 + x;
    }
    code
}

fn fill(row: &[i64], i: usize, next: &mut Vec<i64>, table: &[i64], dead: &mut HashSet<i64>) -> bool {
    if i + 1 == row.len() {
        return build(next, table, dead);
    }
    let mut options = table[(row[i] * 6 + row[i + 1]) as usize];
    let mut block = 0;
    while options > 0 {
        if options & 1 == 1 {
            next.push(block);
            if fill(row, i + 1, next, table, dead) {
                return true;
            }
            next.pop();
        }
        options >>= 1;
        block += 1;
    }
    false
}

fn build(row: &[i64], table: &[i64], dead: &mut HashSet<i64>) -> bool {
    if row.len() == 1 {
        return true;
    }
    let code = row_code(row);
    if dead.contains(&code) {
        return false;
    }
    let mut next: Vec<i64> = Vec::new();
    if fill(row, 0, &mut next, table, dead) {
        return true;
    }
    dead.insert(code);
    false
}

fn pyramid_transition(bottom: String, allowed: Vec<String>) -> bool {
    let mut table = vec![0i64; 36];
    for triple in &allowed {
        let b = triple.as_bytes();
        let pair = (b[0] - b'A') as usize * 6 + (b[1] - b'A') as usize;
        table[pair] |= 1 << (b[2] - b'A');
    }
    let row: Vec<i64> = bottom.bytes().map(|c| (c - b'A') as i64).collect();
    let mut dead: HashSet<i64> = HashSet::new();
    build(&row, &table, &mut dead)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(x: i64) -> char {
    (b'A' + x as u8) as char
}

fn main() {
    let rounds = 200000;
    let mut seed = 756;
    let mut yes = 0;
    let mut check: i64 = 0;
    for round in 0..rounds {
        let mut bottom = String::new();
        for _ in 0..6 {
            bottom.push(letter(next_random(&mut seed) % 6));
        }
        let count = 40 + next_random(&mut seed) % 80;
        let mut allowed: Vec<String> = Vec::new();
        for _ in 0..count {
            let mut t = String::new();
            for _ in 0..3 {
                t.push(letter(next_random(&mut seed) % 6));
            }
            allowed.push(t);
        }
        if pyramid_transition(bottom, allowed) {
            yes += 1;
            check = (check * 31 + round) % 1000000007;
        }
    }
    println!("{rounds} pyramids of width 6: {yes} can be built, checksum {check}");
}
