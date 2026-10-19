// LeetCode 791 — Custom Sort String: the bench, in Rust.
// Mirrors custom_sort_string.kara: count the letters, write out order's
// letters, then the rest in place, into a new String each round.

fn custom_sort_string(order: &str, s: &str) -> String {
    let mut count = [0i64; 26];
    for b in s.bytes() {
        count[(b - b'a') as usize] += 1;
    }
    let mut named = [false; 26];
    let mut out = String::new();
    for c in order.chars() {
        let at = (c as u8 - b'a') as usize;
        named[at] = true;
        for _ in 0..count[at] {
            out.push(c);
        }
    }
    for c in s.chars() {
        if !named[(c as u8 - b'a') as usize] {
            out.push(c);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 791;
    let mut orders: Vec<String> = Vec::new();
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..64 {
        let mut pool = letters.clone();
        let mut i = 25;
        while i > 0 {
            let j = (next_random(&mut seed) % (i + 1)) as usize;
            pool.swap(i as usize, j);
            i -= 1;
        }
        let size = 1 + next_random(&mut seed) % 26;
        orders.push(pool[..size as usize].iter().collect());
        let mut s = String::new();
        for _ in 0..200 {
            s.push(letters[(next_random(&mut seed) % 26) as usize]);
        }
        strings.push(s);
    }
    let rounds = 1000000;
    let mut total = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let answer = custom_sort_string(&orders[r % 64], &strings[(r / 64) % 64]);
        total += answer.len();
        if r % 1000 == 0 {
            for b in answer.bytes() {
                check = (check * 131 + b as i64) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds of 200-letter strings: {total} letters, checksum {check}");
}
