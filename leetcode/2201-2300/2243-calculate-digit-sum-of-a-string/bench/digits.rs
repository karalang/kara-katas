// LeetCode #2243: Calculate Digit Sum of a String -- the benchmark's Rust
// mirror of digits.kara: while the string is longer than k, it is
// rebuilt group by group, each group's digits summed and the sum written
// back.

fn digit_sum(s: &str, k: usize) -> String {
    let mut current = s.to_string();
    while current.len() > k {
        let mut next = String::new();
        let mut start = 0;
        while start < current.len() {
            let end = (start + k).min(current.len());
            let mut sum = 0i64;
            for ch in current[start..end].chars() {
                sum += ch as i64 - '0' as i64;
            }
            next.push_str(&format!("{}", sum));
            start = end;
        }
        current = next;
    }
    current
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn digits_of(seed: &mut i64) -> String {
    (0..100).map(|_| char::from_digit((next_random(seed) % 10) as u32, 10).unwrap()).collect()
}

fn main() {
    let mut seed = 2243i64;
    let mut strings: Vec<String> = (0..1000).map(|_| digits_of(&mut seed)).collect();
    let mut check = 0i64;
    for pass in 0..200 {
        let at = (next_random(&mut seed) % 1000) as usize;
        strings[at] = digits_of(&mut seed);
        let k = pass % 4 + 2;
        for s in strings.iter() {
            for ch in digit_sum(s, k).chars() {
                check = (check * 31 + ch as i64) % 1000000007;
            }
        }
    }
    println!("200 passes over 1000 strings: checksum {}", check);
}
