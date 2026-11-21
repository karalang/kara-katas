// LeetCode #2490: Circular Sentence -- Rust mirror of the ★ arm's benchmark
// (circular.kara): the same 200 sentences and 2300 passes, each letter
// changed and changed back, the sentence collected into a fresh `String`
// for every answer.

fn is_circular_sentence(sentence: &str) -> bool {
    let bytes = sentence.as_bytes();
    let n = bytes.len();
    if bytes[0] != bytes[n - 1] {
        return false;
    }
    for i in 1..n - 1 {
        if bytes[i] == b' ' && bytes[i - 1] != bytes[i + 1] {
            return false;
        }
    }
    true
}

static mut SEED: i64 = 2490;

fn next_random() -> i64 {
    unsafe {
        SEED = (SEED * 1103515245 + 12345) % 2147483648;
        SEED / 65536
    }
}

fn letter(k: i64) -> char {
    (b'a' + (k % 26) as u8) as char
}

fn sentence() -> Vec<char> {
    let mut text: Vec<char> = Vec::new();
    let first = letter(next_random());
    let mut last = first;
    while text.len() < 490 {
        if !text.is_empty() {
            text.push(' ');
        }
        text.push(last);
        for _ in 0..next_random() % 8 {
            text.push(letter(next_random()));
        }
        last = text[text.len() - 1];
    }
    text.push(' ');
    text.push(last);
    text.push(first);
    text
}

fn main() {
    let passes: i64 = 2300;
    let mut sentences: Vec<Vec<char>> = (0..200).map(|_| sentence()).collect();
    let mut check: i64 = 0;
    let mut circular: i64 = 0;
    for p in 0..passes {
        for s in 0..200 {
            let n = sentences[s].len() as i64;
            let at = (check % n) as usize;
            let was = sentences[s][at];
            if was != ' ' {
                sentences[s][at] = letter(check / n + p);
            }
            let text: String = sentences[s].iter().collect();
            let answer = is_circular_sentence(&text);
            sentences[s][at] = was;
            if answer {
                circular += 1;
            }
            check = (check * 31 + if answer { 1 } else { 2 } + p) % 1_000_000_007;
        }
    }
    println!("{} passes over 200 sentences: {} circular, checksum {}", passes, circular, check);
}
