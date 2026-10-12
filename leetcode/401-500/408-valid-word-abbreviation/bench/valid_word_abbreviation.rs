// Benchmark for #408: mirror of valid_word_abbreviation.kara (two
// pointers).

fn valid_word_abbreviation(word: &str, abbr: &str) -> bool {
    let w = word.as_bytes();
    let a = abbr.as_bytes();
    let mut i = 0usize;
    let mut j = 0usize;
    while i < w.len() && j < a.len() {
        if a[j] >= 48 && a[j] <= 57 {
            if a[j] == 48 {
                return false;
            }
            let mut skip = 0usize;
            while j < a.len() && a[j] >= 48 && a[j] <= 57 {
                skip = skip * 10 + (a[j] - 48) as usize;
                j += 1;
            }
            i += skip;
        } else {
            if w[i] != a[j] {
                return false;
            }
            i += 1;
            j += 1;
        }
    }
    i == w.len() && j == a.len()
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: usize = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(20000);
    let rounds = 1000;
    let n: i64 = 20;
    let mut seed: i64 = 408;
    let mut words: Vec<String> = Vec::new();
    let mut abbrs: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut word = String::new();
        for _ in 0..n {
            word.push((97 + step(&mut seed) % 2) as u8 as char);
        }
        let w = word.as_bytes().to_vec();
        let mut abbr = String::new();
        let mut i = 0;
        let mut number = false;
        while i < n {
            if number || step(&mut seed) % 2 == 0 {
                abbr.push(w[i as usize] as char);
                i += 1;
                number = false;
            } else {
                let run = 1 + step(&mut seed) % (n - i);
                abbr.push_str(&run.to_string());
                i += run;
                number = true;
            }
        }
        words.push(word);
        abbrs.push(abbr);
    }
    let mut valid: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let mut found: i64 = 0;
        for i in 0..count {
            if valid_word_abbreviation(&words[i], &abbrs[(i + r) % count]) {
                found += 1;
            }
        }
        valid += found;
        checksum = (checksum * 31 + found) % 1000000007;
    }
    println!("{} words, {} rounds: {} valid, checksum {}", count, rounds, valid, checksum);
}
