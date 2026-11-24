// LeetCode #1320 bench, Rust mirror of the Kāra bench: the ★ arm (one row
// of 27 for the other finger's key, carried from letter to letter) on 100
// words of 300 letters over 2, 5 or 26 letters, built once; then 80
// passes, each setting one letter of every word from the checksum so far,
// answering it and folding the answer plus the pass into the checksum.

fn key_distance(a: i64, b: i64) -> i64 {
    if a == 26 {
        return 0;
    }
    (a / 6 - b / 6).abs() + (a % 6 - b % 6).abs()
}

fn minimum_distance(word: &str) -> i64 {
    let w: Vec<i64> = word.bytes().map(|b| (b - 65) as i64).collect();
    let free = 26;
    let far = 1000000;
    let mut other = vec![far; 27];
    other[free] = 0;
    for i in 1..w.len() {
        let (last, now) = (w[i - 1], w[i]);
        let mut next = vec![far; 27];
        for j in 0..27 {
            if other[j] < far {
                next[j] = next[j].min(other[j] + key_distance(last, now));
                next[last as usize] = next[last as usize].min(other[j] + key_distance(j as i64, now));
            }
        }
        other = next;
    }
    *other.iter().min().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".chars().collect();
    let mut seed = 1320i64;
    let mut words: Vec<Vec<char>> = Vec::new();
    for t in 0..100 {
        let k = if t % 3 == 0 { 2 } else if t % 3 == 1 { 5 } else { 26 };
        let base = next_random(&mut seed) % (27 - k);
        let mut chars: Vec<char> = Vec::new();
        for _ in 0..300 {
            chars.push(letters[(base + next_random(&mut seed) % k) as usize]);
        }
        words.push(chars);
    }
    let mut check: i64 = 0;
    for pass in 0..80i64 {
        for t in 0..100 {
            let chars = &mut words[t];
            chars[(check % 300) as usize] = letters[((check / 7) % 26) as usize];
            let word: String = chars.iter().collect();
            let got = minimum_distance(&word);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    println!("80 passes over 100 words of 300: checksum {}", check);
}
