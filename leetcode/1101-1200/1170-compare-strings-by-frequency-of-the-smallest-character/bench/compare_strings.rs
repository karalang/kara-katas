// LeetCode #1170: Compare Strings by Frequency of the Smallest Character --
// the ★ arm's bench in Rust: words counted by frequency, the counts summed
// from the top down, each query answered by one look-up.

fn f(s: &str) -> i64 {
    let mut smallest = b'z' + 1;
    let mut count = 0;
    for b in s.bytes() {
        if b < smallest {
            smallest = b;
            count = 1;
        } else if b == smallest {
            count += 1;
        }
    }
    count
}

fn num_smaller_by_frequency(queries: &[String], words: &[String]) -> Vec<i64> {
    // above[k]: the words whose frequency is at least k
    let mut above = [0i64; 12];
    for w in words {
        above[f(w) as usize] += 1;
    }
    for k in (0..11).rev() {
        above[k] += above[k + 1];
    }
    queries.iter().map(|q| above[f(q) as usize + 1]).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, letters: i64) -> String {
    let n = 1 + next_random(seed) % 10;
    let mut w = String::new();
    for _ in 0..n {
        w.push((b'a' + (next_random(seed) % letters) as u8) as char);
    }
    w
}

fn main() {
    let rounds = 300;
    let mut seed = 1170;
    let mut queries: Vec<Vec<String>> = Vec::new();
    let mut words: Vec<Vec<String>> = Vec::new();
    for l in 0..16 {
        let letters = [2, 3, 5, 26][l % 4];
        queries.push((0..2000).map(|_| random_word(&mut seed, letters)).collect());
        words.push((0..2000).map(|_| random_word(&mut seed, letters)).collect());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for l in 0..16 {
            let letters = [2, 3, 5, 26][l % 4];
            let i = (next_random(&mut seed) % 2000) as usize;
            queries[l][i] = random_word(&mut seed, letters);
            let j = (next_random(&mut seed) % 2000) as usize;
            words[l][j] = random_word(&mut seed, letters);
            let got = num_smaller_by_frequency(&queries[l], &words[l]);
            for &x in &got {
                total += x;
                check = (check * 131 + x + 1) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over 16 lists of 2000 queries and 2000 words: total {total}, checksum {check}");
}
