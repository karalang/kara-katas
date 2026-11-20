// LeetCode #1662 bench: the ★ arm, two cursors, one in each array.
//
// 20 pairs of word arrays spelling texts of 10^6 letters, cut into words
// of about 8 letters, are built first; half spell the same text and half
// differ in the last letter. Then each pair is checked 20 times.

fn array_strings_are_equal(word1: &[String], word2: &[String]) -> bool {
    let (mut w1, mut i1) = (0usize, 0usize);
    let (mut w2, mut i2) = (0usize, 0usize);
    while w1 < word1.len() && w2 < word2.len() {
        let a = word1[w1].as_bytes();
        let b = word2[w2].as_bytes();
        if a[i1] != b[i2] {
            return false;
        }
        i1 += 1;
        i2 += 1;
        if i1 == a.len() {
            w1 += 1;
            i1 = 0;
        }
        if i2 == b.len() {
            w2 += 1;
            i2 = 0;
        }
    }
    w1 == word1.len() && w2 == word2.len()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(n: usize, seed: &mut i64) -> Vec<u8> {
    (0..n).map(|_| b'a' + (next_random(seed) % 2) as u8).collect()
}

fn cut(text: &[u8], seed: &mut i64) -> Vec<String> {
    let mut words = Vec::new();
    let mut start = 0;
    for i in 1..text.len() {
        if next_random(seed) % 8 == 0 {
            words.push(String::from_utf8(text[start..i].to_vec()).unwrap());
            start = i;
        }
    }
    words.push(String::from_utf8(text[start..].to_vec()).unwrap());
    words
}

fn main() {
    let pairs = 20;
    let letters = 1000000usize;
    let rounds = 20i64;
    let mut seed = 1662i64;
    let mut cases: Vec<(Vec<String>, Vec<String>)> = Vec::new();
    for k in 0..pairs {
        let text = random_text(letters, &mut seed);
        let mut other = text.clone();
        if k % 2 == 1 {
            other[letters - 1] = if other[letters - 1] == b'a' { b'b' } else { b'a' };
        }
        let word1 = cut(&text, &mut seed);
        let word2 = cut(&other, &mut seed);
        cases.push((word1, word2));
    }
    let mut equal = 0;
    let mut check = 0i64;
    for r in 0..rounds {
        for (word1, word2) in cases.iter() {
            let answer = array_strings_are_equal(word1, word2);
            if answer {
                equal += 1;
            }
            check = (check * 31 + if answer { 2 } else { 1 } + word1.len() as i64 + word2.len() as i64 + r) % 1000000007;
        }
    }
    println!("{pairs} pairs of {letters} letters, {rounds} rounds: {equal} equal, checksum {check}");
}
