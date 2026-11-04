// LeetCode #1047: Remove All Adjacent Duplicates In String -- Rust mirror of
// bench/remove_dups.kara: a Vec<char> stack, collected into a String.

fn remove_duplicates(s: &str) -> String {
    let mut stack: Vec<char> = Vec::new();
    for c in s.chars() {
        if stack.last().cloned() == Some(c) {
            stack.pop();
        } else {
            stack.push(c);
        }
    }
    stack.iter().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let n = 200000;
    let rounds = 10;
    let mut seed: i64 = 1047;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        for _ in 0..n {
            s.push((b'a' + (next_random(&mut seed) % 4) as u8) as char);
        }
        strings.push(s);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for s in strings.iter() {
            let answer = remove_duplicates(s);
            let last = match answer.chars().next_back() {
                Some(c) => c as i64,
                None => 0,
            };
            total += answer.len() as i64;
            check = (check * 131 + answer.len() as i64 + last) % 1000000007;
        }
    }
    println!("{count} strings of {n} letters, {rounds} rounds: total length {total}, checksum {check}");
}
