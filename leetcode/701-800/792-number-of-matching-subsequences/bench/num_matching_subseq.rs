// LeetCode 792 — Number of Matching Subsequences: the bench, in Rust.
// Mirrors num_matching_subseq.kara: every word waits in the bucket of
// the next letter it needs, and s is walked once; a bucket is taken
// whole with mem::take, left empty, and walked.

fn num_matching_subseq(s: &str, words: &[String]) -> i64 {
    let mut waiting: Vec<Vec<(usize, usize)>> = vec![Vec::new(); 26];
    for (i, word) in words.iter().enumerate() {
        waiting[(word.as_bytes()[0] - b'a') as usize].push((i, 0));
    }
    let mut count = 0;
    for b in s.bytes() {
        let moving = std::mem::take(&mut waiting[(b - b'a') as usize]);
        for (w, matched) in moving {
            let word = words[w].as_bytes();
            if matched + 1 == word.len() {
                count += 1;
            } else {
                waiting[(word[matched + 1] - b'a') as usize].push((w, matched + 1));
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, len: i64, letters: i64) -> String {
    let mut word = String::new();
    for _ in 0..len {
        word.push((97 + next_random(seed) % letters) as u8 as char);
    }
    word
}

fn main() {
    let mut seed = 792;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..16 {
        let letters = 13 + next_random(&mut seed) % 14;
        strings.push(random_word(&mut seed, 50000, letters));
    }
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..64 {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..5000 {
            let len = 1 + next_random(&mut seed) % 50;
            words.push(random_word(&mut seed, len, 26));
        }
        lists.push(words);
    }
    let rounds = 4000;
    let mut total = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let count = num_matching_subseq(&strings[r % 16], &lists[(r / 16) % 64]);
        total += count;
        check = (check * 131 + count + 1) % 1000000007;
    }
    println!("{rounds} rounds of 5000 words: {total} matching, checksum {check}");
}
