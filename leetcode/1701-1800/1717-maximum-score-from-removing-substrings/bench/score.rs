// LeetCode #1717: Maximum Score From Removing Substrings -- the Rust mirror
// of the bench (score.kara): the pair worth more removed first with a
// stack, then the other pair from what is left, on 20 random strings of
// 100000 letters, each answered 100 times.

fn remove(chars: &[char], first: char, second: char, points: i32) -> (Vec<char>, i32) {
    let mut kept: Vec<char> = Vec::new();
    let mut gained: i32 = 0;
    for &c in chars.iter() {
        if c == second && kept.last().cloned() == Some(first) {
            kept.pop();
            gained += points;
        } else {
            kept.push(c);
        }
    }
    (kept, gained)
}

fn maximum_gain(s: &str, x: i32, y: i32) -> i32 {
    let chars: Vec<char> = s.chars().collect();
    let (first, second, more, less) = if x >= y { ('a', 'b', x, y) } else { ('b', 'a', y, x) };
    let (rest, a) = remove(&chars, first, second, more);
    let (_, b) = remove(&rest, second, first, less);
    a + b
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds: i64 = 100;
    let n = 100000;
    let mut seed: i64 = 1717;
    let mut problems: Vec<(String, i32, i32)> = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        for _ in 0..n {
            let r = next_random(&mut seed) % 200;
            s.push(if r < 2 { 'c' } else if r % 2 == 0 { 'a' } else { 'b' });
        }
        let x = (next_random(&mut seed) % 10000 + 1) as i32;
        let y = (next_random(&mut seed) % 10000 + 1) as i32;
        problems.push((s, x, y));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (s, x, y) in problems.iter() {
            let answer = maximum_gain(s, *x, *y) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} strings of {n} letters, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
