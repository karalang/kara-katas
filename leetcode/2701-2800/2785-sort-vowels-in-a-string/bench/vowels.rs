// LeetCode #2785: Sort Vowels in a String -- the bench in Rust: the ★
// arm over 20 strings of 10^5 letters from all 52, all drawn first, then
// each answered 10 times.

fn is_vowel(c: char) -> bool {
    matches!(c, 'a' | 'e' | 'i' | 'o' | 'u' | 'A' | 'E' | 'I' | 'O' | 'U')
}

fn sort_vowels(s: &str) -> String {
    let mut vowels: Vec<char> = s.chars().filter(|&c| is_vowel(c)).collect();
    vowels.sort();
    let mut next = 0;
    let mut out = String::new();
    for c in s.chars() {
        if is_vowel(c) {
            out.push(vowels[next]);
            next += 1;
        } else {
            out.push(c);
        }
    }
    out
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn random_text(n: i64, from: &str, rng: &mut Rng) -> String {
    let letters: Vec<char> = from.chars().collect();
    (0..n).map(|_| letters[(rng.next_random() % letters.len() as i64) as usize]).collect()
}

fn main() {
    let count = 20;
    let rounds = 10;
    let mut rng = Rng(2785);
    let every = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let cases: Vec<String> = (0..count).map(|_| random_text(100000, every, &mut rng)).collect();
    let mut check = 0i64;
    for r in 0..rounds {
        for s in &cases {
            let t = sort_vowels(s);
            check = t.bytes().fold(check, |c, b| (c * 31 + b as i64) % 1000000007);
            check = (check + r) % 1000000007;
        }
    }
    println!("{count} strings of 10^5, {rounds} rounds: checksum {check}");
}
