// LeetCode #1593: Split a String Into the Max Number of Unique Substrings
// -- the bench in Rust, mirroring unique_split.kara: backtracking over a
// `HashSet<String>` (SipHash, as Kāra's `Set`) of the pieces used.

use std::collections::HashSet;

fn split_from(s: &str, at: usize, used: &mut HashSet<String>, best: &mut usize) {
    if at == s.len() {
        *best = (*best).max(used.len());
        return;
    }
    if used.len() + (s.len() - at) <= *best {
        return;
    }
    for end in at + 1..s.len() + 1 {
        let piece = s[at..end].to_string();
        if !used.contains(&piece) {
            used.insert(piece.clone());
            split_from(s, end, used, best);
            used.remove(&piece);
        }
    }
}

fn max_unique_split(s: &str) -> i32 {
    let mut used = HashSet::new();
    let mut best = 0;
    split_from(s, 0, &mut used, &mut best);
    best as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1593;
    let strings: Vec<String> = (0..20000)
        .map(|_| (0..16).map(|_| (b'a' + (next_random(&mut seed) % 3) as u8) as char).collect())
        .collect();
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for s in &strings {
        let answer = max_unique_split(s) as i64;
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    println!("20000 strings of 16 letters: total {}, checksum {}", total, check);
}
