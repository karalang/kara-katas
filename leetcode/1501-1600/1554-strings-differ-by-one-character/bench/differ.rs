// LeetCode #1554: Strings Differ by One Character -- bench: the ★ arm
// (every word entered once per place with that place blotted out) over 20
// lists of 1000 random words of 100 letters, built once, half of them with
// a pair planted that differs in one place, each asked 3 times. Rust mirror of differ.kara,
// with std's HashSet (SipHash-1-3, as Kāra's Set).

use std::collections::HashSet;

fn differ_by_one(dict: &[String]) -> bool {
    let mut seen: HashSet<String> = HashSet::new();
    for word in dict {
        let letters: Vec<char> = word.chars().collect();
        for j in 0..letters.len() {
            let mut blotted = letters.clone();
            blotted[j] = '*';
            let pattern: String = blotted.iter().collect();
            if !seen.insert(pattern) {
                return true;
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 1554i64;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for l in 0..20 {
        let mut dict = Vec::new();
        for _ in 0..1000 {
            let word: String = (0..100).map(|_| alphabet[(next_random(&mut seed) % 26) as usize]).collect();
            dict.push(word);
        }
        if l % 2 == 1 {
            let at = (next_random(&mut seed) % 1000) as usize;
            let place = (next_random(&mut seed) % 100) as usize;
            let mut letters: Vec<char> = dict[at].chars().collect();
            letters[place] = if letters[place] == 'a' { 'b' } else { 'a' };
            let twin = (next_random(&mut seed) % 1000) as usize;
            dict[twin] = letters.iter().collect();
        }
        lists.push(dict);
    }
    let mut yes = 0i64;
    let mut check = 0i64;
    for pass in 0..3i64 {
        for l in 0..lists.len() {
            if differ_by_one(&lists[l]) {
                yes += 1;
                check = mix(check, pass * 20 + l as i64);
            }
        }
    }
    println!("3 passes over 20 lists of 1000 words of 100 letters: {} true, checksum {}", yes, check);
}
