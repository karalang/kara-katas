// LeetCode #2416: Sum of Prefix Scores of Strings -- the bench, the ★ arm:
// a trie in flat arrays, node k's child by letter c at `next[26 k + c]`
// and `count[k]` the words through it.

fn sum_prefix_scores(words: &[Vec<u8>]) -> Vec<i64> {
    let mut next: Vec<i64> = vec![0; 26];
    let mut count: Vec<i64> = vec![0; 1];
    for w in words {
        let mut at = 0usize;
        for &b in w {
            let c = (b - b'a') as usize;
            if next[26 * at + c] == 0 {
                next[26 * at + c] = count.len() as i64;
                count.push(0);
                next.extend(std::iter::repeat(0).take(26));
            }
            at = next[26 * at + c] as usize;
            count[at] += 1;
        }
    }
    let mut scores = Vec::new();
    for w in words {
        let mut at = 0usize;
        let mut score = 0;
        for &b in w {
            at = next[26 * at + (b - b'a') as usize] as usize;
            score += count[at];
        }
        scores.push(score);
    }
    scores
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2416;
    let mut lists: Vec<Vec<Vec<u8>>> = Vec::new();
    for i in 0..10 {
        let mut words = Vec::new();
        for _ in 0..2000 {
            let len = 1 + next_random(&mut seed) % 50;
            let mut bytes = Vec::new();
            for _ in 0..len {
                bytes.push(b'a' + (next_random(&mut seed) % (2 + 2 * i)) as u8);
            }
            words.push(bytes);
        }
        lists.push(words);
    }
    let mut check: i64 = 0;
    for p in 0..20 {
        for words in lists.iter() {
            for s in sum_prefix_scores(words) {
                check = (check * 31 + s + p) % 1000000007;
            }
        }
    }
    println!("20 passes over 10 lists of 2000 words: checksum {}", check);
}
