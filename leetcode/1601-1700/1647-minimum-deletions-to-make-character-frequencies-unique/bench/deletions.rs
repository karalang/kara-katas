// LeetCode #1647: Minimum Deletions to Make Character Frequencies Unique
// -- the bench's Rust mirror: the ★ arm on 500 random strings of 100000
// letters, each from the first 1 to 26 of the alphabet, all drawn first.

fn min_deletions(s: &str) -> i32 {
    let mut counts = [0i32; 26];
    for b in s.bytes() {
        counts[(b - b'a') as usize] += 1;
    }
    counts.sort();
    counts.reverse();
    let mut deletions = 0;
    let mut cap = counts[0];
    for &c in counts.iter() {
        let keep = c.min(cap);
        deletions += c - keep;
        cap = (keep - 1).max(0);
    }
    deletions
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1647;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..500 {
        let letters = next_random(&mut seed) % 26 + 1;
        let mut s = String::new();
        for _ in 0..100000 {
            s.push((b'a' + (next_random(&mut seed) % letters) as u8) as char);
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for s in &strings {
        let deletions = min_deletions(s) as i64;
        total += deletions;
        check = (check * 31 + deletions + 1) % 1000000007;
    }
    println!("500 strings of 100000 letters: deletions sum to {}, checksum {}", total, check);
}
