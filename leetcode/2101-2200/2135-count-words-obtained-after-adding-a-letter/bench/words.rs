// LeetCode #2135: Count Words Obtained After Adding a Letter -- the
// benchmark, the same algorithm as words.kara.
use std::collections::HashSet;

fn letters(w: &str) -> i64 {
    let mut mask = 0i64;
    for b in w.bytes() {
        mask |= 1 << (b - 97);
    }
    mask
}

fn word_count(start_words: &[String], target_words: &[String]) -> i64 {
    let starts: HashSet<i64> = start_words.iter().map(|w| letters(w)).collect();
    let mut count = 0;
    for w in target_words.iter() {
        let mask = letters(w);
        for b in w.bytes() {
            if starts.contains(&(mask ^ (1 << (b - 97)))) {
                count += 1;
                break;
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(len: i64, k: i64, seed: &mut i64) -> String {
    let mut letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().take(k as usize).collect();
    let mut out = String::new();
    for i in 0..len {
        let j = i + next_random(seed) % (k - i);
        letters.swap(i as usize, j as usize);
        out.push(letters[i as usize]);
    }
    out
}

fn main() {
    let mut seed = 2135i64;
    let mut starts: Vec<Vec<String>> = Vec::new();
    let mut targets: Vec<Vec<String>> = Vec::new();
    for _ in 0..4 {
        let mut s = Vec::new();
        let mut t = Vec::new();
        for _ in 0..50000 {
            let len = next_random(&mut seed) % 6 + 1;
            s.push(word(len, 12, &mut seed));
        }
        for _ in 0..50000 {
            let len = next_random(&mut seed) % 6 + 1;
            t.push(word(len, 12, &mut seed));
        }
        starts.push(s);
        targets.push(t);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..25i64 {
        for p in 0..4 {
            let a = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 50000) as usize;
            let len = next_random(&mut seed) % 6 + 1;
            starts[p][a] = word(len, 12, &mut seed);
            let b = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 50000) as usize;
            let len = next_random(&mut seed) % 6 + 1;
            targets[p][b] = word(len, 12, &mut seed);
            let count = word_count(&starts[p], &targets[p]);
            total += count;
            check = (check * 31 + count + round) % 1000000007;
        }
    }
    println!("100 solves: {} words in all, checksum {}", total, check);
}
