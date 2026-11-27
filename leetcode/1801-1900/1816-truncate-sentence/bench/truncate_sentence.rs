// LeetCode #1816: Truncate Sentence -- the bench in Rust: the ★ arm over
// 2 * 10^6 calls on 1000 sentences of 20 to 100 words, built once, each
// sentence and its k drawn from the checksum so far.

fn truncate_sentence(s: &str, k: i64) -> String {
    let words: Vec<&str> = s.split(' ').take(k as usize).collect();
    words.join(" ")
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1816;
    let mut sentences: Vec<(String, i64)> = Vec::new();
    for _ in 0..1000 {
        let n = 20 + next_random(&mut seed) % 81;
        let mut words: Vec<String> = Vec::new();
        for _ in 0..n {
            let m = 1 + next_random(&mut seed) % 5;
            let mut word = String::new();
            for _ in 0..m {
                word.push((97 + next_random(&mut seed) % 26) as u8 as char);
            }
            words.push(word);
        }
        sentences.push((words.join(" "), n));
    }
    let mut check: i64 = 0;
    for call in 0..2000000i64 {
        let (s, n) = &sentences[((check + call) % 1000) as usize];
        let cut = truncate_sentence(s, 1 + (check + call) % n);
        check = (check * 31 + cut.len() as i64) % 1000000007;
    }
    println!("2000000 calls: checksum {}", check);
}
