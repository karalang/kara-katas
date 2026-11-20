// LeetCode #1750: Minimum Length of String After Deleting Similar Ends --
// the bench (ends.kara in Rust): two pointers.

fn minimum_length(s: &str) -> i32 {
    let b = s.as_bytes();
    let mut left: i64 = 0;
    let mut right: i64 = b.len() as i64 - 1;
    while left < right && b[left as usize] == b[right as usize] {
        let c = b[left as usize];
        while left <= right && b[left as usize] == c {
            left += 1;
        }
        while right >= left && b[right as usize] == c {
            right -= 1;
        }
    }
    (right - left + 1) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// a random middle of up to 1000 letters from `a` and `b`, wrapped in
// layers of one letter on both sides until the string is `n` long
fn draw(n: i64, seed: &mut i64) -> String {
    let alphabet = "ab";
    let mut middle = String::new();
    for _ in 0..next_random(seed) % 1000 {
        let k = (next_random(seed) % 2) as usize;
        middle.push_str(&alphabet[k..k + 1]);
    }
    let mut front: Vec<String> = Vec::new();
    let mut back = String::new();
    let mut size = middle.len() as i64;
    while size < n {
        let k = (next_random(seed) % 2) as usize;
        let letter = &alphabet[k..k + 1];
        let before = next_random(seed) % 3 + 1;
        let after = next_random(seed) % 3 + 1;
        front.push(letter.repeat(before as usize));
        back.push_str(&letter.repeat(after as usize));
        size += before + after;
    }
    let mut s = String::new();
    for layer in front.iter().rev() {
        s.push_str(layer);
    }
    s.push_str(&middle);
    s.push_str(&back);
    s
}

fn main() {
    let count = 50;
    let rounds: i64 = 40;
    let n = 100000;
    let mut seed: i64 = 1750;
    let strings: Vec<String> = (0..count).map(|_| draw(n, &mut seed)).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in strings.iter() {
            let answer = minimum_length(s) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} strings of about {} letters, {} rounds: lengths add to {}, checksum {}", count, n, rounds, sum, check);
}
