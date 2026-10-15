// LeetCode #648: Replace Words -- Rust mirror of the Kāra bench.
//
// The ★ arm over the same inputs and rounds: a trie of the roots as a
// `Vec` of 26-entry child tables, each word walked until the first root
// ends, the words split on spaces and joined back.

fn replace_words(dictionary: &[String], sentence: &str) -> String {
    let mut next: Vec<Vec<usize>> = vec![vec![0; 26]];
    let mut ends: Vec<bool> = vec![false];
    for root in dictionary {
        let mut node = 0;
        for &b in root.as_bytes() {
            let c = (b - b'a') as usize;
            if next[node][c] == 0 {
                next[node][c] = next.len();
                next.push(vec![0; 26]);
                ends.push(false);
            }
            node = next[node][c];
        }
        ends[node] = true;
    }
    let mut out: Vec<String> = Vec::new();
    for word in sentence.split(' ') {
        let bytes = word.as_bytes();
        let mut node = 0;
        let mut length = 0;
        while length < bytes.len() && !ends[node] {
            node = next[node][(bytes[length] - b'a') as usize];
            if node == 0 {
                break;
            }
            length += 1;
        }
        if node != 0 && ends[node] {
            out.push(word[..length].to_string());
        } else {
            out.push(word.to_string());
        }
    }
    out.join(" ")
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(shortest: i64, longest: i64, letters: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    let n = shortest + next_random(seed) % (longest - shortest + 1);
    for _ in 0..n {
        s.push((97 + next_random(seed) % letters) as u8 as char);
    }
    s
}

fn main() {
    let inputs = 20;
    let rounds = 100;
    let mut seed: i64 = 648;
    let mut dictionaries: Vec<Vec<String>> = Vec::new();
    let mut sentences: Vec<String> = Vec::new();
    for _ in 0..inputs {
        let letters = 3 + next_random(&mut seed) % 6;
        let mut roots = Vec::new();
        for _ in 0..1000 {
            roots.push(random_word(3, 6, letters, &mut seed));
        }
        let mut words = Vec::new();
        for _ in 0..20000 {
            words.push(random_word(1, 10, letters, &mut seed));
        }
        dictionaries.push(roots);
        sentences.push(words.join(" "));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let i = (r * 7) % inputs;
        let out = replace_words(&dictionaries[i], &sentences[i]);
        for &b in out.as_bytes() {
            total += 1;
            checksum = (checksum * 31 + b as i64) % 1000000007;
        }
    }
    println!("{} inputs, {} rounds: {} characters, checksum {}", inputs, rounds, total, checksum);
}
