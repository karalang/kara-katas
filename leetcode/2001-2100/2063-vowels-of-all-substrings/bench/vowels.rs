// LeetCode #2063: Vowels of All Substrings -- Rust mirror of the ★ arm's
// benchmark (vowels.kara): one text of 140000 letters, each a vowel with
// chance 40 in 100, and 200 windows of 100000 letters cut from it at a
// random place among its first 32768, each copied out and answered on its
// own.

fn count_vowels(word: String) -> i64 {
    let n = word.len() as i64;
    let mut total = 0i64;
    for (i, c) in word.chars().enumerate() {
        if "aeiou".contains(c) {
            let i = i as i64;
            total += (i + 1) * (n - i);
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let vowels: Vec<char> = "aeiou".chars().collect();
    let others: Vec<char> = "bcdxyz".chars().collect();
    let mut seed = 2063i64;
    let mut text = String::new();
    for _ in 0..140000 {
        if next_random(&mut seed) % 100 < 40 {
            text.push(vowels[(next_random(&mut seed) % 5) as usize]);
        } else {
            text.push(others[(next_random(&mut seed) % 6) as usize]);
        }
    }
    let mut check = 0i64;
    for _ in 0..200 {
        let start = next_random(&mut seed) as usize;
        let a = count_vowels(text[start..start + 100000].to_string());
        check = (check * 31 + a % 1000000007) % 1000000007;
    }
    println!("200 windows: checksum {}", check);
}
