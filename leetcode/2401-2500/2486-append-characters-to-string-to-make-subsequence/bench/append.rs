// LeetCode #2486: Append Characters to String to Make Subsequence --
// bench, Rust mirror of append.kara.

fn append_characters(s: &str, t: &str) -> i64 {
    let wanted: Vec<char> = t.chars().collect();
    let mut matched = 0;
    for c in s.chars() {
        if matched < wanted.len() && c == wanted[matched] {
            matched += 1;
        }
    }
    (wanted.len() - matched) as i64
}

fn main() {
    let mut seed: i64 = 2486;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let letters = ['a', 'b', 'c', 'd'];
    let mut pairs: Vec<(Vec<char>, String)> = Vec::new();
    for _ in 0..20 {
        let s: Vec<char> = (0..10000).map(|_| letters[(next_random() % 4) as usize]).collect();
        let t: String = (0..10000).map(|_| letters[(next_random() % 4) as usize]).collect();
        pairs.push((s, t));
    }
    let mut check: i64 = 0;
    for p in 0..600 {
        for g in 0..20 {
            pairs[g].0[(check % 10000) as usize] = letters[(check / 10000 % 4) as usize];
            let s: String = pairs[g].0.iter().collect();
            check = (check * 31 + append_characters(&s, &pairs[g].1) + p) % 1000000007;
        }
    }
    println!("600 passes over 20 pairs of 10^4 letters: checksum {}", check);
}
