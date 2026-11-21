// LeetCode #2434: Using a Robot to Print the Lexicographically Smallest
// String -- the bench, the ★ arm: the letters left counted, a pointer at
// the smallest with a count, and `t` popped after each push while its
// top is no larger.

fn robot_with_string(b: &[u8]) -> Vec<u8> {
    let mut left = vec![0i64; 26];
    for &c in b.iter() {
        left[(c - b'a') as usize] += 1;
    }
    let mut smallest = 0usize;
    let mut t: Vec<u8> = Vec::new();
    let mut paper: Vec<u8> = Vec::new();
    for &c in b.iter() {
        t.push(c);
        left[(c - b'a') as usize] -= 1;
        while smallest < 26 && left[smallest] == 0 {
            smallest += 1;
        }
        while !t.is_empty() && ((t[t.len() - 1] - b'a') as usize) <= smallest {
            paper.push(t.pop().unwrap());
        }
    }
    paper
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2434;
    let mut word: Vec<u8> = Vec::new();
    for _ in 0..100000 {
        word.push(b'a' + (next_random(&mut seed) % 8) as u8);
    }
    let mut check: i64 = 0;
    for p in 0..300i64 {
        word[((p * 7919) % 100000) as usize] = b'a' + (p % 8) as u8;
        let paper = robot_with_string(&word);
        for &c in paper.iter() {
            check = (check * 31 + c as i64) % 1000000007;
        }
    }
    println!("300 passes over 10^5 letters: checksum {}", check);
}
