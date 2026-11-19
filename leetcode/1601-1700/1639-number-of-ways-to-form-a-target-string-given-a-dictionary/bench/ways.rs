// LeetCode #1639: Number of Ways to Form a Target String Given a
// Dictionary -- the bench's Rust mirror: the ★ arm on 40 random
// dictionaries of 1000 words of 1000 letters and targets of 500 letters,
// all over the letters a to e and drawn first.

const MODULUS: i64 = 1000000007;

fn num_ways(words: &Vec<String>, target: &str) -> i64 {
    let length = words[0].len();
    let goal = target.as_bytes();
    let mut ways = vec![0i64; goal.len() + 1];
    ways[0] = 1;
    for column in 0..length {
        let mut count = [0i64; 26];
        for word in words {
            count[(word.as_bytes()[column] - b'a') as usize] += 1;
        }
        for i in (0..(column + 1).min(goal.len())).rev() {
            let have = count[(goal[i] - b'a') as usize];
            ways[i + 1] = (ways[i + 1] + ways[i] * have) % MODULUS;
        }
    }
    ways[goal.len()]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(length: usize, seed: &mut i64) -> String {
    let mut word = String::with_capacity(length);
    for _ in 0..length {
        word.push((b'a' + (next_random(seed) % 5) as u8) as char);
    }
    word
}

fn main() {
    let mut seed: i64 = 1639;
    let mut cases = Vec::new();
    for _ in 0..40 {
        let mut words = Vec::new();
        for _ in 0..1000 {
            words.push(random_word(1000, &mut seed));
        }
        let target = random_word(500, &mut seed);
        cases.push((words, target));
    }
    let mut check: i64 = 0;
    for (words, target) in &cases {
        let ways = num_ways(words, target);
        check = (check * 31 + ways + 1) % 1000000007;
    }
    println!("40 dictionaries of 1000 words: checksum {}", check);
}
