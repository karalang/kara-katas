// Benchmark for #604: Rust mirror of the ★ arm (read as you go); see
// string_iterator.kara. The text is copied into a `Vec<char>`, as the
// Kāra arm collects it.

struct StringIterator {
    text: Vec<char>,
    at: usize,
    current: char,
    left: i64,
}

impl StringIterator {
    fn new(compressed: &str) -> StringIterator {
        StringIterator { text: compressed.chars().collect(), at: 0, current: ' ', left: 0 }
    }

    fn next(&mut self) -> char {
        if self.left == 0 {
            if self.at == self.text.len() {
                return ' ';
            }
            self.current = self.text[self.at];
            self.at += 1;
            let mut count = 0;
            while self.at < self.text.len() && self.text[self.at].is_ascii_digit() {
                count = count * 10 + (self.text[self.at] as i64 - 48);
                self.at += 1;
            }
            self.left = count;
        }
        self.left -= 1;
        self.current
    }

    fn has_next(&self) -> bool {
        self.left > 0 || self.at < self.text.len()
    }
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000;
    let rounds = 200;
    let mut seed: i64 = 604;
    let mut texts: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut text = String::new();
        loop {
            let k = step(&mut seed) % 52;
            let letter = if k < 26 { (65 + k) as u8 as char } else { (97 + k - 26) as u8 as char };
            let n = if step(&mut seed) % 10 == 0 {
                let hi = step(&mut seed);
                let lo = step(&mut seed);
                1 + (hi * 32768 + lo) % 1000000000
            } else {
                1 + step(&mut seed) % 20
            };
            let run = format!("{}{}", letter, n);
            if text.len() + run.len() > 1000 {
                break;
            }
            text.push_str(&run);
        }
        texts.push(text);
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let mut it = StringIterator::new(&texts[(round * 7 + g) % count]);
            for _ in 0..50 {
                if it.has_next() {
                    total += 1;
                }
                let c = it.next();
                checksum = (checksum * 31 + c as i64) % 1000000007;
            }
        }
    }
    println!("{} texts, {} rounds: {} letters left, checksum {}", count, rounds, total, checksum);
}
