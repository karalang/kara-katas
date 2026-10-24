// Benchmark: LeetCode #966 Vowel Spellchecker -- the ★ arm, three maps,
// on cases of 5000 words and 5000 queries, LeetCode's largest. Mirrors
// spellchecker.kara, .c, .py and go-seq/. The maps are std's `HashSet`
// and `HashMap`, SipHash-1-3 like Kāra's.
use std::collections::{HashMap, HashSet};

fn devowel(w: &str) -> String {
    let mut out = String::with_capacity(w.len());
    for c in w.to_lowercase().chars() {
        if c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' {
            out.push('*');
        } else {
            out.push(c);
        }
    }
    out
}

fn spellchecker(wordlist: &[String], queries: &[String]) -> Vec<String> {
    let mut exact: HashSet<String> = HashSet::new();
    let mut by_case: HashMap<String, String> = HashMap::new();
    let mut by_vowel: HashMap<String, String> = HashMap::new();
    for w in wordlist {
        exact.insert(w.clone());
        by_case.entry(w.to_lowercase()).or_insert(w.clone());
        by_vowel.entry(devowel(w)).or_insert(w.clone());
    }
    let mut out = Vec::new();
    for q in queries {
        if exact.contains(q) {
            out.push(q.clone());
        } else if let Some(w) = by_case.get(&q.to_lowercase()) {
            out.push(w.clone());
        } else if let Some(w) = by_vowel.get(&devowel(q)) {
            out.push(w.clone());
        } else {
            out.push(String::new());
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn spell(letters: &[i64]) -> String {
    let alphabet: Vec<char> = "aeioukbAEIOUKB".chars().collect();
    letters.iter().map(|&x| alphabet[x as usize]).collect()
}

fn random_word(len: i64, seed: &mut i64) -> Vec<i64> {
    (0..len).map(|_| next_random(seed) % 14).collect()
}

fn query_from(w: &[i64], kind: i64, max_len: i64, seed: &mut i64) -> Vec<i64> {
    if kind == 3 {
        let len = 1 + next_random(seed) % max_len;
        return random_word(len, seed);
    }
    let mut q = w.to_vec();
    for x in q.iter_mut() {
        if kind == 1 && next_random(seed) % 2 == 0 {
            *x = (*x + 7) % 14;
        } else if kind == 2 && *x % 7 < 5 && next_random(seed) % 2 == 0 {
            let a = next_random(seed) % 5;
            *x = a + 7 * (next_random(seed) % 2);
        }
    }
    q
}

fn fold(s: &str, check: i64) -> i64 {
    let mut h = check;
    for b in s.bytes() {
        h = (h * 131 + b as i64) % 1000000007;
    }
    (h * 131 + 1) % 1000000007
}

fn random_case(n: i64, m: i64, max_len: i64, seed: &mut i64) -> (Vec<String>, Vec<String>) {
    let mut ws: Vec<Vec<i64>> = Vec::new();
    for _ in 0..n {
        let len = 1 + next_random(seed) % max_len;
        ws.push(random_word(len, seed));
    }
    let mut qs = Vec::new();
    for _ in 0..m {
        let w = ws[(next_random(seed) % n) as usize].clone();
        let kind = next_random(seed) % 4;
        qs.push(spell(&query_from(&w, kind, max_len, seed)));
    }
    (ws.iter().map(|w| spell(w)).collect(), qs)
}

fn main() {
    let rounds = 200;
    let mut seed = 966;
    let mut wls = Vec::new();
    let mut qss = Vec::new();
    for _ in 0..5 {
        let (wl, qs) = random_case(5000, 5000, 7, &mut seed);
        wls.push(wl);
        qss.push(qs);
    }
    let mut matched = 0;
    let mut check = 0;
    for r in 0..rounds {
        let got = spellchecker(&wls[r % 5], &qss[r % 5]);
        for g in &got {
            if !g.is_empty() {
                matched += 1;
            }
            check = fold(g, check);
        }
    }
    println!("{rounds} rounds over 5 cases of 5000 words and 5000 queries: {matched} matched, checksum {check}");
}
