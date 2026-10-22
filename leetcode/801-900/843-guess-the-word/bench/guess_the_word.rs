// Benchmark for #843: Guess the Word -- Rust twin of the Kāra ★ arm
// (minimax over the words still possible).

struct Master {
    words: Vec<String>,
    secret: String,
    guesses: i64,
    found: bool,
}

impl Master {
    fn guess(&mut self, word: &str) -> i64 {
        self.guesses += 1;
        if !self.words.iter().any(|w| w == word) {
            return -1;
        }
        if word == self.secret && self.guesses <= 10 {
            self.found = true;
        }
        let a = word.as_bytes();
        let b = self.secret.as_bytes();
        (0..6).filter(|&k| a[k] == b[k]).count() as i64
    }
}

fn shared(a: &[u8], b: &[u8]) -> i64 {
    let mut count = 0;
    for k in 0..a.len() {
        if a[k] == b[k] {
            count += 1;
        }
    }
    count
}

fn find_secret_word(words: &[String], master: &mut Master) {
    let n = words.len();
    let letters: Vec<Vec<u8>> = words.iter().map(|w| w.as_bytes().to_vec()).collect();
    let mut same: Vec<Vec<i64>> = Vec::new();
    for i in 0..n {
        let mut row = Vec::new();
        for j in 0..n {
            row.push(shared(&letters[i], &letters[j]));
        }
        same.push(row);
    }
    let mut possible: Vec<usize> = (0..n).collect();
    while !possible.is_empty() {
        let mut best = possible[0];
        let mut best_worst = n as i64 + 1;
        for &c in possible.iter() {
            let mut groups = [0i64; 7];
            for &o in possible.iter() {
                groups[same[c][o] as usize] += 1;
            }
            let mut worst = 0;
            for k in 0..6 {
                worst = worst.max(groups[k]);
            }
            if worst < best_worst {
                best_worst = worst;
                best = c;
            }
        }
        let answer = master.guess(&words[best]);
        if answer == 6 {
            return;
        }
        let mut left = Vec::new();
        for &o in possible.iter() {
            if same[best][o] == answer {
                left.push(o);
            }
        }
        possible = left;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64usize;
    let rounds = 6000usize;
    let mut seed: i64 = 843;
    let mut lists: Vec<Vec<String>> = Vec::new();
    let mut masters: Vec<Master> = Vec::new();
    for g in 0..count {
        let k = [4, 8, 16, 26][g % 4];
        let mut words: Vec<String> = Vec::new();
        while words.len() < 100 {
            let mut w = String::new();
            for _ in 0..6 {
                w.push((97 + next_random(&mut seed) % k) as u8 as char);
            }
            if !words.contains(&w) {
                words.push(w);
            }
        }
        let secret = words[(next_random(&mut seed) % 100) as usize].clone();
        masters.push(Master { words: words.clone(), secret, guesses: 0, found: false });
        lists.push(words);
    }
    let mut found = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = round % count;
        masters[g].guesses = 0;
        masters[g].found = false;
        find_secret_word(&lists[g], &mut masters[g]);
        if masters[g].found {
            found += 1;
        }
        checksum = (checksum * 31 + masters[g].guesses) % 1000000007;
    }
    println!("{rounds} rounds of {count} lists: {found} found, checksum {checksum}");
}
