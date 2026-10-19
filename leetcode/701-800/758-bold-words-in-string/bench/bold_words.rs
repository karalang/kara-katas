// LeetCode 758 — Bold Words in String: benchmark, the ★ arm in Rust.

fn bold_words(words: &[String], s: &str) -> String {
    let n = s.len();
    let mut bold = vec![false; n];
    for word in words {
        let mut from = 0;
        while from < n {
            match s[from..].find(word.as_str()) {
                Some(at) => {
                    for i in from + at..from + at + word.len() {
                        bold[i] = true;
                    }
                    from = from + at + 1;
                }
                None => break,
            }
        }
    }
    let mut out = String::new();
    let chars: Vec<char> = s.chars().collect();
    for i in 0..n {
        if bold[i] && (i == 0 || !bold[i - 1]) {
            out.push_str("<b>");
        }
        out.push(chars[i]);
        if bold[i] && (i == n - 1 || !bold[i + 1]) {
            out.push_str("</b>");
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(seed: &mut i64, length: i64, letters: i64) -> String {
    let mut text = String::new();
    for _ in 0..length {
        text.push((b'a' + (next_random(seed) % letters) as u8) as char);
    }
    text
}

fn main() {
    let rounds = 20000;
    let mut seed = 758;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let s = random_text(&mut seed, 500, 4);
        let mut words: Vec<String> = Vec::new();
        for _ in 0..50 {
            let size = 1 + next_random(&mut seed) % 10;
            words.push(random_text(&mut seed, size, 5));
        }
        let answer = bold_words(&words, &s);
        total += answer.len() as i64;
        for c in answer.bytes() {
            check = (check * 31 + c as i64) % 1000000007;
        }
    }
    println!("{rounds} strings of 500 letters: {total} characters out, checksum {check}");
}
