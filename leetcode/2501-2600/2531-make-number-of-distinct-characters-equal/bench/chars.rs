// LeetCode #2531: Make Number of Distinct Characters Equal -- Rust mirror of
// the benchmark (chars.kara): the same pairs, passes, order and checksum.

fn distinct(counts: &[i64; 26]) -> i64 {
    counts.iter().filter(|&&c| c > 0).count() as i64
}

fn is_it_possible(word1: &str, word2: &str) -> bool {
    let mut one = [0i64; 26];
    let mut two = [0i64; 26];
    for b in word1.bytes() {
        one[(b - b'a') as usize] += 1;
    }
    for b in word2.bytes() {
        two[(b - b'a') as usize] += 1;
    }
    for a in 0..26 {
        for b in 0..26 {
            if one[a] > 0 && two[b] > 0 {
                one[a] -= 1;
                one[b] += 1;
                two[b] -= 1;
                two[a] += 1;
                let equal = distinct(&one) == distinct(&two);
                one[a] += 1;
                one[b] -= 1;
                two[b] += 1;
                two[a] -= 1;
                if equal {
                    return true;
                }
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, length: i64, letters: i64) -> String {
    let mut word = String::new();
    for _ in 0..length {
        word.push((b'a' + (next_random(seed) % letters) as u8) as char);
    }
    word
}

fn main() {
    let mut seed = 2531;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..1000 {
        let l1 = next_random(&mut seed) % 1000 + 1;
        let k1 = next_random(&mut seed) % 26 + 1;
        let word1 = random_word(&mut seed, l1, k1);
        let l2 = next_random(&mut seed) % 1000 + 1;
        let k2 = next_random(&mut seed) % 26 + 1;
        let word2 = random_word(&mut seed, l2, k2);
        pairs.push((word1, word2));
    }
    let passes = 24;
    let mut check: i64 = 0;
    for p in 0..passes {
        let start = check % 1000;
        for i in 0..1000 {
            let (word1, word2) = &pairs[((start + i) % 1000) as usize];
            let answer = is_it_possible(word1, word2);
            check = (check * 31 + if answer { 2 } else { 1 } + p) % 1000000007;
        }
    }
    println!("{passes} passes over 1000 pairs of words: checksum {check}");
}
