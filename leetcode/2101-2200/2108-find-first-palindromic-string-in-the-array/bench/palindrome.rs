// LeetCode #2108: Find First Palindromic String in the Array -- the
// benchmark, the same algorithm as palindrome.kara: each word's bytes read
// from both ends towards the middle.

fn is_palindrome(w: &str) -> bool {
    let b = w.as_bytes();
    let mut i: i64 = 0;
    let mut j: i64 = b.len() as i64 - 1;
    while i < j {
        if b[i as usize] != b[j as usize] {
            return false;
        }
        i += 1;
        j -= 1;
    }
    true
}

fn first_palindrome(words: &[String]) -> String {
    for w in words {
        if is_palindrome(w) {
            return w.clone();
        }
    }
    String::new()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 2108;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..200 {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..100 {
            let mut letters: Vec<i64> = (0..50).map(|_| next_random(&mut seed) % 26).collect();
            for i in 0..50 {
                letters.push(letters[49 - i]);
            }
            if next_random(&mut seed) % 200 != 0 {
                let at = (25 + next_random(&mut seed) % 50) as usize;
                letters[at] = (letters[at] + 1 + next_random(&mut seed) % 25) % 26;
            }
            words.push(letters.iter().map(|&l| alphabet[l as usize]).collect());
        }
        lists.push(words);
    }
    let mut found: i64 = 0;
    let mut letters_total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..50 {
        for words in &lists {
            let got = first_palindrome(words);
            if !got.is_empty() {
                found += 1;
            }
            letters_total += got.len() as i64;
            for c in got.chars().take(3) {
                check = (check * 31 + c as i64) % 1000000007;
            }
            check = (check * 31 + got.len() as i64) % 1000000007;
        }
    }
    println!("10000 searches: {} found, {} letters, checksum {}", found, letters_total, check);
}
