// LeetCode #1417 bench, Rust: the letters and the digits apart, each in its
// order, woven together from the larger group, workload and checksum as
// reformat.kara.

fn reformat(s: &str) -> String {
    let letters: Vec<char> = s.chars().filter(|c| c.is_ascii_lowercase()).collect();
    let digits: Vec<char> = s.chars().filter(|c| c.is_ascii_digit()).collect();
    if letters.len().abs_diff(digits.len()) > 1 {
        return String::new();
    }
    let (first, second) = if digits.len() > letters.len() { (digits, letters) } else { (letters, digits) };
    let mut out = String::new();
    for i in 0..first.len() {
        out.push(first[i]);
        if i < second.len() {
            out.push(second[i]);
        }
    }
    out
}

fn main() {
    let mut seed: i64 = 1417;
    let mut pool = String::new();
    let letters = ['a', 'b', 'c', 'x', 'y', 'z'];
    for _ in 0..100000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let r = seed / 65536;
        let letter = letters[(r % 6) as usize];
        let digit = format!("{}", r / 6 % 10);
        if r / 60 % 2 == 0 {
            pool.push(letter);
            pool.push_str(&digit);
        } else {
            pool.push_str(&digit);
            pool.push(letter);
        }
    }
    let mut check: i64 = 0;
    for _ in 0..20000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let start = (2 * (seed / 65536 % 99750)) as usize;
        let out = reformat(&pool[start..start + 500]);
        let mut sum: i64 = 0;
        for &b in out.as_bytes() {
            sum = (sum * 31 + b as i64) % 1000000007;
        }
        check = (check * 131 + sum) % 1000000007;
    }
    println!("20000 windows of 500 characters: checksum {}", check);
}
