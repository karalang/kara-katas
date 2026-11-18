// LeetCode #2309: Greatest English Letter in Upper and Lower Case -- the
// bench, the ★ arm in Rust. A mask of the lowercase letters and one of
// the uppercase; the highest bit of their `&` is the answer.

fn greatest_letter(s: &str) -> String {
    let mut lower = 0i64;
    let mut upper = 0i64;
    for b in s.bytes() {
        if b >= b'a' {
            lower |= 1 << (b - b'a');
        } else {
            upper |= 1 << (b - b'A');
        }
    }
    let both = lower & upper;
    for i in (0..26).rev() {
        if (both >> i) & 1 == 1 {
            return ((b'A' + i as u8) as char).to_string();
        }
    }
    String::new()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".chars().collect();
    let mut seed = 2309;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..1000 {
        let pool = next_random(&mut seed) % 30 + 1;
        let from: Vec<char> = (0..pool).map(|_| letters[(next_random(&mut seed) % 52) as usize]).collect();
        let mut s = String::new();
        for _ in 0..1000 {
            s.push(from[(next_random(&mut seed) % pool) as usize]);
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    for _ in 0..100 {
        for s in &strings {
            let letter = greatest_letter(s);
            let code = if letter.is_empty() { 0 } else { letter.as_bytes()[0] as i64 };
            check = (check * 31 + code) % 1000000007;
        }
    }
    println!("100 passes over 1000 strings of 1000 letters: checksum {}", check);
}
