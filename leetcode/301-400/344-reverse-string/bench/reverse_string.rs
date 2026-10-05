// Benchmark workload for LeetCode #344 — Rust mirror of reverse_string.kara.

const LEN: i64 = 200000;
const PUNCHES: i64 = 4000;
const MODULUS: i64 = 1073741789;

fn reverse_string(s: &mut [char]) {
    if s.len() < 2 {
        return;
    }
    let mut i = 0;
    let mut j = s.len() - 1;
    while i < j {
        let t = s[i];
        s[i] = s[j];
        s[j] = t;
        i += 1;
        j -= 1;
    }
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(k: i64) -> char {
    if k < 16 {
        return (97 + k) as u8 as char;
    }
    char::from_u32((945 + k - 16) as u32).unwrap()
}

fn main() {
    let mut seed = 344;
    let mut s: Vec<char> = Vec::new();
    for _ in 0..LEN {
        s.push(letter(next(&mut seed) % 32));
    }
    let mut sink: i64 = 0;
    for _ in 0..PUNCHES {
        let pos = ((next(&mut seed) * 32768 + next(&mut seed)) % LEN) as usize;
        s[pos] = letter(next(&mut seed) % 32);
        reverse_string(&mut s);
        let at = ((next(&mut seed) * 32768 + next(&mut seed)) % LEN) as usize;
        sink = (sink * 31 + s[at] as i64) % MODULUS;
    }
    println!("sink {sink}");
}
