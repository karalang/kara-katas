// LeetCode 748 — Shortest Completing Word, bench: the ★ arm (letter
// counts) on a list of 1000 words that keeps changing, against a new
// plate each round. Mirrors shortest_completing_word.kara.

fn shortest_completing_word(license_plate: &str, words: &[String]) -> String {
    let mut need = [0i64; 26];
    for &c in license_plate.as_bytes() {
        if c.is_ascii_lowercase() {
            need[(c - b'a') as usize] += 1;
        } else if c.is_ascii_uppercase() {
            need[(c - b'A') as usize] += 1;
        }
    }
    let mut best: Option<usize> = None;
    for (i, w) in words.iter().enumerate() {
        if let Some(b) = best {
            if w.len() >= words[b].len() {
                continue;
            }
        }
        let mut have = [0i64; 26];
        for &c in w.as_bytes() {
            have[(c - b'a') as usize] += 1;
        }
        if (0..26).all(|c| have[c] >= need[c]) {
            best = Some(i);
        }
    }
    words[best.unwrap()].clone()
}

struct Rng(i64);
impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn random_word(r: &mut Rng) -> String {
    let n = 1 + r.next() % 15;
    (0..n).map(|_| (97 + r.next() % 6) as u8 as char).collect()
}

fn random_plate(r: &mut Rng) -> String {
    let n = 1 + r.next() % 7;
    let mut s = String::new();
    for _ in 0..n {
        let kind = r.next() % 6;
        let code = if kind < 2 {
            97 + r.next() % 6
        } else if kind < 4 {
            65 + r.next() % 6
        } else if kind == 4 {
            48 + r.next() % 10
        } else {
            32
        };
        s.push(code as u8 as char);
    }
    s
}

fn main() {
    let rounds = 100000;
    let n = 1000;
    let mut r = Rng(748);
    let mut words: Vec<String> = (0..n).map(|_| random_word(&mut r)).collect();
    let mut letters = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for _ in 0..5 {
            let i = (r.next() % (n as i64 - 1)) as usize;
            words[i] = random_word(&mut r);
        }
        let plate = random_plate(&mut r);
        let mut last = String::new();
        for &c in plate.as_bytes() {
            if c.is_ascii_lowercase() {
                last.push(c as char);
            } else if c.is_ascii_uppercase() {
                last.push((c + 32) as char);
            }
        }
        if last.is_empty() {
            last.push('a');
        }
        words[n - 1] = last;
        let got = shortest_completing_word(&plate, &words);
        letters += got.len() as i64;
        for &b in got.as_bytes() {
            check = (check * 31 + b as i64) % 1000000007;
        }
    }
    println!("{} plates against 1000 words: answers {} letters long in all, checksum {}", rounds, letters, check);
}
