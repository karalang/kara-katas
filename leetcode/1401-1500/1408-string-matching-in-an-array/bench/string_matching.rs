// LeetCode #1408 bench, Rust: the same check of every word against every
// other, workload and checksum as string_matching.kara.

fn string_matching(words: &Vec<String>) -> Vec<String> {
    words.iter().filter(|w| words.iter().any(|other| other != *w && other.contains(w.as_str()))).cloned().collect()
}

fn main() {
    let mut seed: i64 = 1408;
    let mut pool: Vec<String> = Vec::new();
    for _ in 0..10000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let size = 1 + seed / 65536 % 12;
        let mut word = String::new();
        for _ in 0..size {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            word.push((b'a' + (seed / 65536 % 3) as u8) as char);
        }
        pool.push(word);
    }
    let mut check: i64 = 0;
    for r in 0..2000i64 {
        let at = ((check + r * 7919) % 9901) as usize;
        let mut words: Vec<String> = Vec::new();
        for w in pool[at..at + 100].iter() {
            if !words.contains(w) {
                words.push(w.clone());
            }
        }
        let found = string_matching(&words);
        let letters: i64 = found.iter().map(|w| w.len() as i64).sum();
        check = (check * 131 + found.len() as i64 * 1000 + letters) % 1000000007;
    }
    println!("2000 windows of 100 words: checksum {}", check);
}
