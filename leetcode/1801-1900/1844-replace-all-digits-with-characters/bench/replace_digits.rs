// LeetCode #1844: Replace All Digits with Characters -- the bench in Rust: the ★ arm over
// 500000 calls on 40 strings of 100 places, built once, each call's string
// drawn from the checksum so far and one byte of its output, at a place
// drawn the same way, folded in. Each call builds its own output string.

fn replace_digits(s: &str) -> String {
    let letters = s.as_bytes();
    let mut out = String::new();
    for i in 0..letters.len() {
        if i % 2 == 0 {
            out.push(letters[i] as char);
        } else {
            out.push((letters[i - 1] + letters[i] - b'0') as char);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1844;
    let mut cases: Vec<String> = Vec::new();
    for _ in 0..40 {
        let mut s = String::new();
        let mut letter: i64 = 0;
        for i in 0..100 {
            if i % 2 == 0 {
                letter = next_random(&mut seed) % 26;
                s.push((b'a' + letter as u8) as char);
            } else {
                let most = (25 - letter).min(9);
                s.push((b'0' + (next_random(&mut seed) % (most + 1)) as u8) as char);
            }
        }
        cases.push(s);
    }
    let mut check: i64 = 0;
    for call in 0..500000i64 {
        let out = replace_digits(&cases[((check + call) % 40) as usize]);
        check = (check * 31 + out.as_bytes()[((check / 40 + call) % 100) as usize] as i64) % 1000000007;
    }
    println!("500000 calls: checksum {}", check);
}
