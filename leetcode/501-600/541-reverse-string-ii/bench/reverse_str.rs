// Benchmark for #541: Rust mirror of the ★ arm (two pointers over the
// characters); see reverse_str.kara.

fn reverse_str(s: &str, k: usize) -> String {
    let mut chars: Vec<char> = s.chars().collect();
    let n = chars.len();
    let mut start = 0;
    while start < n {
        let mut i = start;
        let mut j = (start + k).min(n) - 1;
        while i < j {
            chars.swap(i, j);
            i += 1;
            j -= 1;
        }
        start += 2 * k;
    }
    chars.iter().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 200 random words of 10,000 letters (the problem's longest) built
    // once. Then 100 times over every word is answered with a k from 1
    // to 500 picked by the round and the word, and one letter of the
    // answer, picked the same way, goes into the checksum.
    let words = 200;
    let mut seed: i64 = 541;
    let mut all: Vec<String> = Vec::new();
    for _ in 0..words {
        let w: String = (0..10000).map(|_| (b'a' + (next_random(&mut seed) % 26) as u8) as char).collect();
        all.push(w);
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for r in 0..100usize {
        for t in 0..words {
            let k = 1 + (r * 37 + t * 11) % 500;
            let answer = reverse_str(&all[t], k);
            let letter = answer.as_bytes()[(r * 7 + t * 13) % 10000] as i64;
            total += answer.len();
            checksum = (checksum * 31 + letter) % 1000000007;
        }
    }
    println!("{words} words, 100 times each: {total} letters, checksum {checksum}");
}
