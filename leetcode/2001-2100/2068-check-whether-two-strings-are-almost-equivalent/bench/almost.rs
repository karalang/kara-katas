// LeetCode #2068: Check Whether Two Strings are Almost Equivalent -- Rust
// mirror of the ★ arm's benchmark (almost.kara): every pair of 1500 words
// of 100 letters, each a common word of `a`, `b` and `c` with up to 30
// letters changed.

fn check_almost_equivalent(word1: &str, word2: &str) -> bool {
    let mut diff = [0i64; 26];
    for b in word1.bytes() {
        diff[(b - b'a') as usize] += 1;
    }
    for b in word2.bytes() {
        diff[(b - b'a') as usize] -= 1;
    }
    diff.iter().all(|d| d.abs() <= 3)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters = [b'a', b'b', b'c'];
    let mut seed = 2068;
    let mut base = Vec::new();
    for _ in 0..100 {
        base.push(letters[(next_random(&mut seed) % 3) as usize]);
    }
    let mut words: Vec<String> = Vec::new();
    for _ in 0..1500 {
        let mut word = base.clone();
        for _ in 0..next_random(&mut seed) % 31 {
            let i = (next_random(&mut seed) % 100) as usize;
            word[i] = letters[(next_random(&mut seed) % 3) as usize];
        }
        words.push(String::from_utf8(word).unwrap());
    }
    let mut yes = 0;
    let mut check: i64 = 0;
    for i in 0..1500 {
        for j in i + 1..1500 {
            if check_almost_equivalent(&words[i], &words[j]) {
                yes += 1;
                check = (check * 31 + (i * 1500 + j) as i64) % 1000000007;
            }
        }
    }
    println!("1124250 pairs: {} almost equivalent, checksum {}", yes, check);
}
