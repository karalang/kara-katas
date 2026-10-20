// LeetCode 809 -- Expressive Words: the bench, with the ★ arm's two
// pointers over the groups.
fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn stretchy(s: &str, word: &str) -> bool {
    let a = s.as_bytes();
    let b = word.as_bytes();
    let (mut i, mut j) = (0, 0);
    while i < a.len() && j < b.len() {
        let c = a[i];
        if b[j] != c {
            return false;
        }
        let from_i = i;
        while i < a.len() && a[i] == c {
            i += 1;
        }
        let from_j = j;
        while j < b.len() && b[j] == c {
            j += 1;
        }
        let (in_s, in_word) = (i - from_i, j - from_j);
        if in_s < in_word || (in_s > in_word && in_s < 3) {
            return false;
        }
    }
    i == a.len() && j == b.len()
}

fn expressive_words(s: &str, words: &[String]) -> i64 {
    let mut count = 0;
    for w in words {
        if stretchy(s, w) {
            count += 1;
        }
    }
    count
}

fn spell(groups: &[(u8, i64)]) -> String {
    let mut out = String::new();
    for &(c, n) in groups {
        for _ in 0..n {
            out.push(c as char);
        }
    }
    out
}

fn main() {
    let mut seed = 809;
    let mut texts: Vec<String> = Vec::new();
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..64 {
        let mut groups: Vec<(u8, i64)> = Vec::new();
        let mut last = 26;
        for _ in 0..25 {
            let mut c = next_random(&mut seed) % 5;
            if c == last {
                c = (c + 1) % 5;
            }
            last = c;
            groups.push(((97 + c) as u8, 1 + next_random(&mut seed) % 4));
        }
        let mut words: Vec<String> = Vec::new();
        for _ in 0..100 {
            if next_random(&mut seed) % 4 == 0 {
                let n = 1 + next_random(&mut seed) % 100;
                let mut word = String::new();
                for _ in 0..n {
                    word.push((97 + next_random(&mut seed) % 5) as u8 as char);
                }
                words.push(word);
            } else {
                let mut shrunk: Vec<(u8, i64)> = Vec::new();
                for &(c, n) in &groups {
                    shrunk.push((c, if n >= 3 { 1 + next_random(&mut seed) % n } else { n }));
                }
                if next_random(&mut seed) % 3 == 0 {
                    let g = (next_random(&mut seed) % 25) as usize;
                    shrunk[g].1 = groups[g].1 + 1;
                }
                words.push(spell(&shrunk));
            }
        }
        texts.push(spell(&groups));
        lists.push(words);
    }
    let rounds: i64 = 200000;
    let (mut total, mut check) = (0i64, 0i64);
    for r in 0..rounds {
        let k = (r % 64) as usize;
        let n = expressive_words(&texts[k], &lists[k]);
        total += n;
        check = (check * 131 + n + r) % 1000000007;
    }
    println!("{} rounds of 100 words: {} stretchy, checksum {}", rounds, total, check);
}
