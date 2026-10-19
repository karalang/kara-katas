// LeetCode 804 -- Unique Morse Code Words: the bench, mirroring
// unique_morse.kara with the same set of strings.
use std::collections::HashSet;

const CODES: [&str; 26] = [
    ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.",
    "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..",
];

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// The word written in Morse code, its letters' codes run together.
fn morse(word: &str) -> String {
    let mut out = String::new();
    for b in word.bytes() {
        out.push_str(CODES[(b - 97) as usize]);
    }
    out
}

fn unique_morse_representations(words: &[String]) -> i64 {
    let mut seen: HashSet<String> = HashSet::new();
    for word in words.iter() {
        seen.insert(morse(word));
    }
    seen.len() as i64
}

fn main() {
    let mut seed: i64 = 804;
    let letters = b"abcdefghijklmnopqrstuvwxyz";
    let short = b"etianm";
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..64 {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..100 {
            let length = 1 + next_random(&mut seed) % 12;
            let few = next_random(&mut seed) % 2 == 0;
            let mut word = String::new();
            for _ in 0..length {
                if few {
                    word.push(short[(next_random(&mut seed) % 6) as usize] as char);
                } else {
                    word.push(letters[(next_random(&mut seed) % 26) as usize] as char);
                }
            }
            words.push(word);
        }
        lists.push(words);
    }
    let rounds: i64 = 100000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let k = unique_morse_representations(&lists[(r % 64) as usize]);
        total += k;
        check = (check * 131 + k) % 1000000007;
    }
    println!("{} rounds of 100 words: {} codes in all, checksum {}", rounds, total, check);
}
