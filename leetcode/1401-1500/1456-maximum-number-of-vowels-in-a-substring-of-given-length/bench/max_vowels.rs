// LeetCode #1456 bench mirror: a window of k letters slid along the
// string, its vowels counted as a letter comes in and another goes out.

fn max_vowels(s: &str, k: i32) -> i32 {
    let letters: Vec<char> = s.chars().collect();
    let k = k as usize;
    let is_vowel = |c: char| "aeiou".contains(c);
    let mut count: i32 = 0;
    for i in 0..k {
        if is_vowel(letters[i]) {
            count += 1;
        }
    }
    let mut best = count;
    for i in k..letters.len() {
        if is_vowel(letters[i]) {
            count += 1;
        }
        if is_vowel(letters[i - k]) {
            count -= 1;
        }
        best = best.max(count);
    }
    best
}

fn main() {
    // 200 strings of 10^5 letters, a vowel one time in 3, drawn once, each
    // asked for windows of 1 to 10^5 letters 5 times, the answers folded to
    // a checksum
    let mut seed: i64 = 1456;
    let vowels: Vec<char> = "aeiou".chars().collect();
    let others: Vec<char> = "bcdfghjklmnpqrstvwxyz".chars().collect();
    let mut texts: Vec<String> = Vec::new();
    for _ in 0..200 {
        let mut s = String::new();
        for _ in 0..100000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let odd = seed / 65536 % 3 == 0;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let pick = seed / 65536;
            s.push(if odd { vowels[(pick % 5) as usize] } else { others[(pick % 21) as usize] });
        }
        texts.push(s);
    }
    let mut check: i64 = 0;
    for _ in 0..5 {
        for s in texts.iter() {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let k = 1 + seed / 65536 % 100000;
            check = (check * 131 + max_vowels(s, k as i32) as i64) % 1000000007;
        }
    }
    println!("1000 windows of 10^5 letters: checksum {}", check);
}
