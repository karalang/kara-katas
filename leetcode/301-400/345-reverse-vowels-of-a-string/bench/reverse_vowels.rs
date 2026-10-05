// Benchmark workload for LeetCode #345 — Rust mirror of reverse_vowels.kara.

const LEN: i64 = 200000;
const PUNCHES: i64 = 1000;
const MODULUS: i64 = 1073741789;

fn is_vowel(c: char) -> bool {
    matches!(c, 'a' | 'e' | 'i' | 'o' | 'u' | 'A' | 'E' | 'I' | 'O' | 'U')
}

fn reverse_vowels(cs: &mut [char]) {
    let mut i = 0i64;
    let mut j = cs.len() as i64 - 1;
    while i < j {
        if !is_vowel(cs[i as usize]) {
            i += 1;
        } else if !is_vowel(cs[j as usize]) {
            j -= 1;
        } else {
            cs.swap(i as usize, j as usize);
            i += 1;
            j -= 1;
        }
    }
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(k: i64) -> char {
    if k < 26 {
        return (97 + k) as u8 as char;
    }
    (65 + k - 26) as u8 as char
}

fn main() {
    let mut seed = 345i64;
    let mut s: Vec<char> = Vec::new();
    for _ in 0..LEN {
        s.push(letter(next(&mut seed) % 32));
    }
    let mut sink = 0i64;
    for _ in 0..PUNCHES {
        let pos = (next(&mut seed) * 32768 + next(&mut seed)) % LEN;
        s[pos as usize] = letter(next(&mut seed) % 32);
        reverse_vowels(&mut s);
        let at = (next(&mut seed) * 32768 + next(&mut seed)) % LEN;
        sink = (sink * 31 + s[at as usize] as u32 as i64) % MODULUS;
    }
    println!("sink {}", sink);
}
