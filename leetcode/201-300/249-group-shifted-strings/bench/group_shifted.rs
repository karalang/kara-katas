// Benchmark workload for LeetCode #249 — Group Shifted Strings (Rust mirror).
// Mirrors group_shifted.kara algorithm-for-algorithm, including the two map
// probes per word (contains_key, then entry) that the Kara version performs.
use std::collections::HashMap;

fn canonical(word: &str) -> String {
    let bytes = word.as_bytes();
    let n = bytes.len();
    if n == 0 {
        return String::new();
    }
    let shift = bytes[0] as i64 - b'a' as i64;
    let mut out = String::new();
    for i in 0..n {
        let c = ((bytes[i] as i64 - b'a' as i64 - shift) + 26) % 26;
        out.push_str(&format!("{},", c));
    }
    out
}

fn main() {
    let words_n: i64 = 120000;
    let rounds: i64 = 5;

    let mut words: Vec<String> = Vec::new();
    let mut state: i64 = 249249;
    for _ in 0..words_n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let len = (state / 65536) % 10 + 3;
        state = (state * 1103515245 + 12345) & 2147483647;
        let seed = (state / 65536) % 40;
        state = (state * 1103515245 + 12345) & 2147483647;
        let shift = (state / 65536) % 26;

        let mut s = String::new();
        for i in 0..len {
            let base = (seed * 7 + i * 11) % 26;
            let ch = (base + shift) % 26;
            s.push((97 + ch) as u8 as char);
        }
        words.push(s);
    }

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        let mut table: HashMap<String, Vec<String>> = HashMap::new();
        let mut groups: i64 = 0;
        let mut keysum: i64 = 0;
        for w in &words {
            let key = canonical(w);
            for &c in key.as_bytes() {
                keysum = (keysum * 31 + c as i64) % 1000000007;
            }
            if !table.contains_key(&key) {
                groups += 1;
            }
            table.entry(key).or_insert_with(Vec::new).push(w.clone());
        }
        sink = (sink * 131 + groups) % 1000000007;
        sink = (sink * 31 + keysum) % 1000000007;
    }
    println!("{}", sink);
}
