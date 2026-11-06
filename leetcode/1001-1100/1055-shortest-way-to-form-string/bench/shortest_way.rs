// LeetCode #1055: Shortest Way to Form String -- Rust mirror of
// bench/shortest_way.kara.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn shortest_way(source: &str, target: &str) -> i64 {
    let s = source.as_bytes();
    let t = target.as_bytes();
    let mut pieces = 0;
    let mut i = 0;
    while i < t.len() {
        let start = i;
        for &c in s {
            if i < t.len() && t[i] == c {
                i += 1;
            }
        }
        if i == start {
            return -1;
        }
        pieces += 1;
    }
    pieces
}

fn random_word(n: i64, seed: &mut i64) -> String {
    let mut word = String::new();
    for _ in 0..n {
        word.push((97 + next_random(seed) % 20) as u8 as char);
    }
    word
}

fn main() {
    let count = 100;
    let rounds = 10;
    let mut seed = 1055;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..count {
        let source = random_word(1000, &mut seed);
        let target = random_word(10000, &mut seed);
        pairs.push((source, target));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for (source, target) in pairs.iter() {
            let answer = shortest_way(source, target);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    println!("{count} pairs of 1000 and 10000 letters, {rounds} rounds: total {total}, checksum {check}");
}
