// LeetCode #1190 bench: the ★ arm in Rust, over the same 200 strings of
// about 2000 characters and 200 rounds as the Kāra bench.

fn reverse_parentheses(s: &str) -> String {
    let bytes = s.as_bytes();
    let n = bytes.len();
    let mut pair = vec![0usize; n];
    let mut open: Vec<usize> = Vec::new();
    for i in 0..n {
        if bytes[i] == b'(' {
            open.push(i);
        } else if bytes[i] == b')' {
            let j = open.pop().unwrap();
            pair[i] = j;
            pair[j] = i;
        }
    }
    let mut out = String::with_capacity(n);
    let mut i: i64 = 0;
    let mut step: i64 = 1;
    while i < n as i64 {
        let b = bytes[i as usize];
        if b == b'(' || b == b')' {
            i = pair[i as usize] as i64;
            step = -step;
        } else {
            out.push(b as char);
        }
        i += step;
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_case(seed: &mut i64, n: usize, letters: &[char]) -> String {
    let mut s = String::new();
    let mut open = 0;
    for _ in 0..n {
        let r = next_random(seed) % 4;
        if r == 0 {
            s.push('(');
            open += 1;
        } else if r == 1 && open > 0 {
            s.push(')');
            open -= 1;
        } else {
            s.push(letters[(next_random(seed) % letters.len() as i64) as usize]);
        }
    }
    for _ in 0..open {
        s.push(')');
    }
    s
}

fn nested(seed: &mut i64, depth: usize, letters: &[char]) -> String {
    let mut s = String::new();
    for _ in 0..depth {
        s.push(letters[(next_random(seed) % letters.len() as i64) as usize]);
        s.push('(');
    }
    for _ in 0..depth {
        s.push(letters[(next_random(seed) % letters.len() as i64) as usize]);
        s.push(')');
    }
    s
}

fn digest(s: &str) -> i64 {
    let mut h: i64 = 0;
    for b in s.bytes() {
        h = (h * 131 + b as i64) % 1000000007;
    }
    h
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 1190;
    let cases: Vec<String> = (0..200)
        .map(|i| {
            if i % 2 == 0 {
                random_case(&mut seed, 2000, &letters)
            } else {
                nested(&mut seed, 500, &letters)
            }
        })
        .collect();
    let mut check: i64 = 0;
    for _ in 0..200 {
        for s in &cases {
            check = (check * 131 + digest(&reverse_parentheses(s))) % 1000000007;
        }
    }
    println!("200 rounds of 200 strings of about 2000 characters: checksum {check}");
}
