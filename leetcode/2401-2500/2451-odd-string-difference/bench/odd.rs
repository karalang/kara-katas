// LeetCode #2451: Odd String Difference -- the bench, the ★ arm: the
// common difference array read off the first three words, and the word
// whose array is not it.

fn differences(word: &str) -> Vec<i64> {
    let b = word.as_bytes();
    let mut steps: Vec<i64> = Vec::new();
    for j in 1..b.len() {
        steps.push(b[j] as i64 - b[j - 1] as i64);
    }
    steps
}

fn odd_string(words: &[String]) -> String {
    let a = differences(&words[0]);
    let b = differences(&words[1]);
    let c = differences(&words[2]);
    let common = if a == b || a == c { a } else { b };
    for w in words.iter() {
        if differences(w) != common {
            return w.clone();
        }
    }
    words[0].clone()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word_of(steps: &[i64], seed: &mut i64) -> String {
    let mut at = 0;
    let mut low = 0;
    let mut high = 0;
    for &s in steps.iter() {
        at += s;
        low = low.min(at);
        high = high.max(at);
    }
    let mut code = -low + next_random(seed) % (26 - (high - low));
    let mut letters: Vec<u8> = vec![(97 + code) as u8];
    for &s in steps.iter() {
        code += s;
        letters.push((97 + code) as u8);
    }
    String::from_utf8(letters).unwrap()
}

fn main() {
    let mut seed = 2451;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..2000 {
        let common: Vec<i64> = (0..19).map(|_| next_random(&mut seed) % 3 - 1).collect();
        let mut other = common.clone();
        other[18] += 1;
        let odd = next_random(&mut seed) % 100;
        let mut words: Vec<String> = Vec::new();
        for i in 0..100 {
            words.push(word_of(if i == odd { &other } else { &common }, &mut seed));
        }
        lists.push(words);
    }
    let mut check: i64 = 0;
    for p in 0..110usize {
        for c in 0..lists.len() {
            lists[c].swap(0, (p + c) % 100);
            let answer = odd_string(&lists[c]);
            for &x in answer.as_bytes().iter() {
                check = (check * 31 + x as i64 + p as i64) % 1000000007;
            }
        }
    }
    println!("110 passes over 2000 lists of 100 words: checksum {}", check);
}
