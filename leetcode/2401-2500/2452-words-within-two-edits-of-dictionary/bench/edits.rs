// LeetCode #2452: Words Within Two Edits of Dictionary -- the bench, the
// ★ arm: each query against each word, the differing places counted
// until a third rules the word out.

fn within_two(query: &str, word: &str) -> bool {
    let a = query.as_bytes();
    let b = word.as_bytes();
    let mut differ = 0;
    for j in 0..a.len() {
        if a[j] != b[j] {
            differ += 1;
            if differ > 2 {
                return false;
            }
        }
    }
    true
}

fn two_edit_words(queries: &[String], dictionary: &[String]) -> Vec<String> {
    let mut answers: Vec<String> = Vec::new();
    for q in queries.iter() {
        for w in dictionary.iter() {
            if within_two(q, w) {
                answers.push(q.clone());
                break;
            }
        }
    }
    answers
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64) -> Vec<u8> {
    (0..100).map(|_| (97 + next_random(seed) % 4) as u8).collect()
}

fn main() {
    let mut seed = 2452;
    let mut dictionaries: Vec<Vec<String>> = Vec::new();
    let mut queries: Vec<Vec<Vec<u8>>> = Vec::new();
    for _ in 0..100 {
        let words: Vec<Vec<u8>> = (0..100).map(|_| random_word(&mut seed)).collect();
        let mut asks: Vec<Vec<u8>> = Vec::new();
        for _ in 0..100 {
            let mut b = words[(next_random(&mut seed) % 100) as usize].clone();
            for _ in 0..next_random(&mut seed) % 5 {
                let place = (next_random(&mut seed) % 100) as usize;
                b[place] = (97 + next_random(&mut seed) % 4) as u8;
            }
            asks.push(b);
        }
        dictionaries.push(words.iter().map(|w| String::from_utf8(w.clone()).unwrap()).collect());
        queries.push(asks);
    }
    let mut check: i64 = 0;
    for p in 0..45usize {
        for c in 0..100 {
            let place = (next_random(&mut seed) % 100) as usize;
            queries[c][p % 100][place] = (97 + next_random(&mut seed) % 4) as u8;
            let asks: Vec<String> = queries[c].iter().map(|q| String::from_utf8(q.clone()).unwrap()).collect();
            let kept = two_edit_words(&asks, &dictionaries[c]);
            check = (check * 31 + kept.len() as i64 + p as i64) % 1000000007;
        }
    }
    println!("45 passes over 100 cases of 100 queries: checksum {}", check);
}
