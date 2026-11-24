// LeetCode #1309 bench in Rust: the ★ arm (the code read from the right, a
// `#` taking the two digits before it) on the same 200 codes and 500 passes.

fn freq_alphabets(s: &str) -> String {
    let b = s.as_bytes();
    let mut letters: Vec<char> = Vec::new();
    let mut i = b.len() as i64 - 1;
    while i >= 0 {
        let number = if b[i as usize] == b'#' {
            i -= 3;
            (b[(i + 1) as usize] - b'0') * 10 + (b[(i + 2) as usize] - b'0')
        } else {
            i -= 1;
            b[(i + 1) as usize] - b'0'
        };
        letters.push((b'a' + number - 1) as char);
    }
    letters.reverse();
    letters.iter().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn encode(letters: &[i64]) -> String {
    let mut code = String::new();
    for &k in letters {
        if k < 9 {
            code.push_str(&format!("{}", k + 1));
        } else {
            code.push_str(&format!("{}#", k + 1));
        }
    }
    code
}

fn main() {
    let mut seed = 1309i64;
    let mut texts: Vec<Vec<i64>> = Vec::new();
    let mut codes: Vec<String> = Vec::new();
    for _ in 0..200 {
        let letters: Vec<i64> = (0..300).map(|_| next_random(&mut seed) % 26).collect();
        codes.push(encode(&letters));
        texts.push(letters);
    }
    let mut check: i64 = 0;
    for pass in 0..500i64 {
        let t = (check % 200) as usize;
        texts[t][((check / 200) % 300) as usize] = (check / 7) % 26;
        codes[t] = encode(&texts[t]);
        for code in &codes {
            let got = freq_alphabets(code);
            let b = got.as_bytes();
            check = (check * 31 + b[(check % b.len() as i64) as usize] as i64 + b.len() as i64 + pass) % 1000000007;
        }
    }
    println!("500 passes over 200 codes: checksum {check}");
}
