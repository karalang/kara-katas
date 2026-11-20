// LeetCode #1698: Number of Distinct Substrings in a String -- the bench's
// Rust mirror: the ★ arm on 100 random strings of 500 letters, each from
// the first 2 to 26 letters of the alphabet, all drawn first, each
// answered 3 times.

fn count_distinct(s: &str) -> i32 {
    let letters = s.as_bytes();
    let mut children: Vec<Vec<i64>> = vec![vec![0; 26]];
    let mut made = 0;
    for start in 0..letters.len() {
        let mut node = 0usize;
        for &c in letters[start..].iter() {
            let edge = (c - b'a') as usize;
            if children[node][edge] == 0 {
                children.push(vec![0; 26]);
                children[node][edge] = (children.len() - 1) as i64;
                made += 1;
            }
            node = children[node][edge] as usize;
        }
    }
    made
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let rounds = 3;
    let n = 500;
    let alphabet = b"abcdefghijklmnopqrstuvwxyz";
    let mut seed = 1698;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let used = next_random(&mut seed) % 25 + 2;
        let mut s = String::new();
        for _ in 0..n {
            s.push(alphabet[(next_random(&mut seed) % used) as usize] as char);
        }
        strings.push(s);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in strings.iter() {
            let answer = count_distinct(s) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} strings of {n} letters, {rounds} rounds: answers sum to {total}, checksum {check}");
}
