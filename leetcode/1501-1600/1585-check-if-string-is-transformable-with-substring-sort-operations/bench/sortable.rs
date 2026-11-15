// LeetCode #1585 bench: the same first-unused-copy match, in Rust.
use std::collections::VecDeque;

fn is_transformable(s: &str, t: &str) -> bool {
    let mut at: Vec<VecDeque<i64>> = vec![VecDeque::new(); 10];
    for (i, c) in s.bytes().enumerate() {
        at[(c - b'0') as usize].push_back(i as i64);
    }
    for c in t.bytes() {
        let d = (c - b'0') as usize;
        let p = match at[d].pop_front() {
            Some(p) => p,
            None => return false,
        };
        for e in 0..d {
            if let Some(&q) = at[e].front() {
                if q < p {
                    return false;
                }
            }
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n = 100000i64;
    let mut seed = 1585i64;
    let mut problems: Vec<(String, String)> = Vec::new();
    for k in 0..40 {
        let mut s: Vec<u8> = Vec::new();
        for _ in 0..n {
            s.push(b'0' + (next_random(&mut seed) % 10) as u8);
        }
        let mut t = s.clone();
        for _ in 0..2000 {
            let a = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % (n - 50)) as usize;
            let b = a + (next_random(&mut seed) % 50 + 1) as usize;
            t[a..b].sort();
        }
        if k % 2 == 1 {
            let a = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % n) as usize;
            let b = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % n) as usize;
            t.swap(a, b);
        }
        problems.push((String::from_utf8(s).unwrap(), String::from_utf8(t).unwrap()));
    }
    let (mut check, mut yes) = (0i64, 0i64);
    for (s, t) in problems.iter() {
        let ok = is_transformable(s, t);
        if ok {
            yes += 1;
        }
        check = mix(check, if ok { 1 } else { 0 });
    }
    println!("40 problems of 100000 digits: {} transformable, checksum {}", yes, check);
}
