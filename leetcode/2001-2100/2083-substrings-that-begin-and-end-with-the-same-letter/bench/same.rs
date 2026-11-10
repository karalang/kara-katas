// LeetCode #2083: Substrings That Begin and End With the Same Letter --
// Rust mirror of the ★ arm's benchmark (same.kara): one text of 10^6
// letters built once, then 5000 windows of 10^5 letters counted through a
// `&str` view of the text.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn number_of_substrings(s: &str) -> i64 {
    let mut counts = [0i64; 26];
    for b in s.bytes() {
        counts[(b - b'a') as usize] += 1;
    }
    counts.iter().map(|&c| c * (c + 1) / 2).sum()
}

fn main() {
    let letters = "abcdefghijklmnopqrstuvwxyz";
    let mut seed = 2083;
    let mut text = String::new();
    for _ in 0..1000000 {
        let at = (next_random(&mut seed) % 26 * (next_random(&mut seed) % 26) / 25) as usize;
        text.push_str(&letters[at..at + 1]);
    }
    let (mut total, mut check) = (0i64, 0i64);
    for _ in 0..5000 {
        let from = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 900001) as usize;
        let a = number_of_substrings(&text[from..from + 100000]);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("5000 windows: sum {}, checksum {}", total, check);
}
