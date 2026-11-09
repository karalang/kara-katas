// LeetCode #1078 bench, Rust mirror of occurrences.kara: the same texts,
// bigrams, rounds and checksum.

fn find_occurrences(text: &str, first: &str, second: &str) -> Vec<String> {
    let words: Vec<&str> = text.split(' ').collect();
    let mut out = Vec::new();
    for i in 2..words.len() {
        if words[i - 2] == first && words[i - 1] == second {
            out.push(words[i].to_string());
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(longest: i64, k: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    let n = next_random(seed) % longest + 1;
    for _ in 0..n {
        s.push((b'a' + (next_random(seed) % k) as u8) as char);
    }
    s
}

fn main() {
    let rounds = 300;
    let mut seed: i64 = 1078;
    let vocabulary: Vec<String> = (0..12).map(|_| random_word(4, 3, &mut seed)).collect();
    let mut texts: Vec<String> = Vec::new();
    let mut firsts: Vec<String> = Vec::new();
    let mut seconds: Vec<String> = Vec::new();
    let mut owner: Vec<usize> = Vec::new();
    for t in 0..100 {
        let mut words: Vec<String> = Vec::new();
        let mut length: i64 = -1;
        loop {
            let w = vocabulary[(next_random(&mut seed) % 12) as usize].clone();
            if length + 1 + w.len() as i64 > 1000 {
                break;
            }
            length += 1 + w.len() as i64;
            words.push(w);
        }
        for _ in 0..8 {
            if next_random(&mut seed) % 4 < 3 {
                let at = (next_random(&mut seed) % (words.len() as i64 - 1)) as usize;
                firsts.push(words[at].clone());
                seconds.push(words[at + 1].clone());
            } else {
                firsts.push(vocabulary[(next_random(&mut seed) % 12) as usize].clone());
                seconds.push(vocabulary[(next_random(&mut seed) % 12) as usize].clone());
            }
            owner.push(t);
        }
        texts.push(words.join(" "));
    }
    let queries = firsts.len();
    let mut found: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for j in 0..queries {
            let q = (j * 7 + r) % queries;
            let out = find_occurrences(&texts[owner[q]], &firsts[q], &seconds[q]);
            found += out.len() as i64;
            for w in &out {
                for &c in w.as_bytes() {
                    check = (check * 31 + c as i64) % 1000000007;
                }
            }
            check = (check * 31 + out.len() as i64) % 1000000007;
        }
    }
    println!("{} rounds of {} bigrams over 100 texts: {} words found, checksum {}", rounds, queries, found, check);
}
