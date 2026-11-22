// LeetCode #2810: Faulty Keyboard -- the bench in Rust: the ★ arm over
// 20000 strings of 100 letters, about a fifth of them i, all drawn first,
// then each typed 10 times.

fn final_string(s: &str) -> String {
    let mut screen = String::new();
    for c in s.chars() {
        if c == 'i' {
            screen = screen.chars().rev().collect();
        } else {
            screen.push(c);
        }
    }
    screen
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn digest(s: &str) -> i64 {
    s.bytes().fold(0, |h, b| (h * 131 + b as i64) % 1000000007)
}

fn main() {
    let count = 20000;
    let rounds = 10;
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut rng = Rng(2810);
    let mut cases = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        for _ in 0..100 {
            let r = rng.next_random() % 125;
            s.push(if r < 25 { 'i' } else { letters[(r % 26) as usize] });
        }
        cases.push(s);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for s in &cases {
            let out = final_string(s);
            total += out.len() as i64;
            check = (check * 31 + digest(&out) + r) % 1000000007;
        }
    }
    println!("{count} strings of 100, {rounds} rounds: lengths sum to {total}, checksum {check}");
}
