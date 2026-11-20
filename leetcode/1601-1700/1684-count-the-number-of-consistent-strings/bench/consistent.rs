// LeetCode #1684: Count the Number of Consistent Strings -- the bench's
// Rust mirror: the ★ arm on 100 random problems of 10000 words, all drawn
// first, each answered 20 times.

fn count_consistent(allowed: &str, words: &[String]) -> i32 {
    let mut ok = [false; 26];
    for b in allowed.bytes() {
        ok[(b - b'a') as usize] = true;
    }
    let mut count = 0;
    for word in words {
        if word.bytes().all(|b| ok[(b - b'a') as usize]) {
            count += 1;
        }
    }
    count
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let size = 10000;
    let rounds = 20;
    let alphabet = b"abcdefghijklmnopqrstuvwxyz";
    let mut seed = 1684;
    let mut problems: Vec<(String, Vec<String>)> = Vec::new();
    for _ in 0..count {
        let mut allowed = String::new();
        for &b in alphabet.iter() {
            if next_random(&mut seed) % 8 != 0 {
                allowed.push(b as char);
            }
        }
        if allowed.is_empty() {
            allowed.push('a');
        }
        let mut words = Vec::new();
        for _ in 0..size {
            let length = next_random(&mut seed) % 10 + 1;
            let mut word = String::new();
            for _ in 0..length {
                word.push(alphabet[(next_random(&mut seed) % 26) as usize] as char);
            }
            words.push(word);
        }
        problems.push((allowed, words));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (allowed, words) in problems.iter() {
            let answer = count_consistent(allowed, words) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} problems of {size} words, {rounds} rounds: {total} consistent, checksum {check}");
}
