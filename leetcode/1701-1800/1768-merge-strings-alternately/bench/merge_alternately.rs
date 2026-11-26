// LeetCode #1768: Merge Strings Alternately -- the bench in Rust, mirroring
// merge_alternately.kara: the words' letters as `Vec<char>`, one index
// walking both.
fn merge_alternately(word1: &str, word2: &str) -> String {
    let a: Vec<char> = word1.chars().collect();
    let b: Vec<char> = word2.chars().collect();
    let mut merged = String::new();
    for i in 0..a.len().max(b.len()) {
        if i < a.len() {
            merged.push(a[i]);
        }
        if i < b.len() {
            merged.push(b[i]);
        }
    }
    merged
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1768;
    let mut words: Vec<String> = Vec::new();
    for _ in 0..1000 {
        let n = 1 + next_random(&mut seed) % 100;
        let mut s = String::new();
        for _ in 0..n {
            s.push(char::from_u32((97 + next_random(&mut seed) % 26) as u32).unwrap());
        }
        words.push(s);
    }
    let mut check: i64 = 0;
    for call in 0..2000000i64 {
        let a = ((check + call * 7919) % 1000) as usize;
        let b = ((check / 3 + call * 104729) % 1000) as usize;
        let merged = merge_alternately(&words[a], &words[b]);
        let at = (check % merged.len() as i64) as usize;
        check = (check * 31 + merged.len() as i64 + merged.as_bytes()[at] as i64) % 1000000007;
    }
    println!("2000000 calls over 1000 words: checksum {}", check);
}
