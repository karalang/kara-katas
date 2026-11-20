// LeetCode #1754: Largest Merge Of Two Strings -- the bench (merge.kara in
// Rust): the larger rest goes first.

fn largest_merge(word1: &str, word2: &str) -> String {
    let mut merge = String::new();
    let mut i = 0;
    let mut j = 0;
    while i < word1.len() || j < word2.len() {
        if word1[i..] > word2[j..] {
            merge.push_str(&word1[i..i + 1]);
            i += 1;
        } else {
            merge.push_str(&word2[j..j + 1]);
            j += 1;
        }
    }
    merge
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// `n` letters, `a` but for a `b` one time in 300, so that the two rests
// often tie for a long way
fn word(n: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    for _ in 0..n {
        s.push_str(if next_random(seed) % 300 == 0 { "b" } else { "a" });
    }
    s
}

fn main() {
    let count = 200;
    let rounds: i64 = 20;
    let n = 3000;
    let mut seed: i64 = 1754;
    let pairs: Vec<(String, String)> = (0..count)
        .map(|_| {
            let word1 = word(n, &mut seed);
            let word2 = word(n, &mut seed);
            (word1, word2)
        })
        .collect();
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (word1, word2) in pairs.iter() {
            let merge = largest_merge(word1, word2);
            check = (check * 31 + r) % 1000000007;
            for &b in merge.as_bytes() {
                check = (check * 31 + b as i64) % 1000000007;
            }
        }
    }
    println!("{} pairs of {} letters, {} rounds: checksum {}", count, n, rounds, check);
}
