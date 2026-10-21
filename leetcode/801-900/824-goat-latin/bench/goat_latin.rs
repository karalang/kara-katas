// Benchmark for #824: Goat Latin -- the ★ arm (split, growing suffix).
//
// Mirrors goat_latin.kara: the sentence split at spaces, each word keeping
// a first vowel and moving a first consonant to the end, then "ma" and a
// run of 'a's kept in a string that grows by one letter per word.

fn is_vowel(c: char) -> bool {
    "aeiouAEIOU".contains(c)
}

fn to_goat_latin(sentence: &str) -> String {
    let mut answer = String::new();
    let mut tail = String::new();
    for word in sentence.split(' ') {
        tail.push('a');
        if !answer.is_empty() {
            answer.push(' ');
        }
        let first = word.chars().next().unwrap();
        if is_vowel(first) {
            answer.push_str(word);
        } else {
            answer.push_str(&word[first.len_utf8()..]);
            answer.push(first);
        }
        answer.push_str("ma");
        answer.push_str(&tail);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64usize;
    let rounds = 2000000usize;
    let letters = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let mut seed: i64 = 824;
    let mut sentences: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        loop {
            let length = 1 + next_random(&mut seed) % 9;
            let extra = if s.is_empty() { length } else { length + 1 };
            if s.len() as i64 + extra > 150 {
                break;
            }
            if !s.is_empty() {
                s.push(' ');
            }
            for _ in 0..length {
                s.push(letters[(next_random(&mut seed) % 52) as usize] as char);
            }
        }
        sentences.push(s);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let answer = to_goat_latin(&sentences[round % count]);
        total += answer.len() as i64;
        let bytes = answer.as_bytes();
        checksum = (checksum * 131 + bytes[round % bytes.len()] as i64) % 1000000007;
    }
    println!("{rounds} rounds of {count} sentences: total {total}, checksum {checksum}");
}
