// LeetCode #1119: Remove Vowels from a String -- the bench in Rust, the
// ★ arm's filter over the same 64 texts and 2000 rounds.

fn remove_vowels(s: String) -> String {
    s.chars()
        .filter(|c| match c {
            'a' | 'e' | 'i' | 'o' | 'u' => false,
            _ => true,
        })
        .collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 1119;
    let mut texts: Vec<Vec<char>> = Vec::new();
    for _ in 0..64 {
        texts.push((0..1000).map(|_| letters[(next_random(&mut seed) % 26) as usize]).collect());
    }
    let mut kept: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..2000usize {
        for j in 0..texts.len() {
            let at = (round * 7919 + j * 104729) % 1000;
            texts[j][at] = letters[(round + j) % 26];
            let s: String = texts[j].iter().collect();
            let r = remove_vowels(s);
            kept += r.len() as i64;
            check = (check * 31 + r.len() as i64 + r.chars().next().map_or(0, |c| c as i64)) % 1000000007;
        }
    }
    println!("2000 rounds over 64 texts of 1000 letters: {} letters kept, checksum {}", kept, check);
}
