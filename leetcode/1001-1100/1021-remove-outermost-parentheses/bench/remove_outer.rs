// LeetCode #1021: Remove Outermost Parentheses -- bench
// Mirrors ./remove_outer.kara; see ../README.md § Benchmarks.

fn remove_outer_parentheses(s: &str) -> String {
    let mut out = String::new();
    let mut depth = 0i64;
    for c in s.chars() {
        if c == '(' {
            if depth > 0 {
                out.push(c);
            }
            depth += 1;
        } else {
            depth -= 1;
            if depth > 0 {
                out.push(c);
            }
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let rounds = 30;
    let mut seed = 1021;
    let mut strings: Vec<String> = Vec::new();
    let mut chars = 0;
    for _ in 0..count {
        let pairs = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 50000 + 1;
        let open = 2 + next_random(&mut seed) % 5;
        let mut s = String::new();
        let mut left = pairs;
        let mut depth = 0;
        while left > 0 || depth > 0 {
            let opens = if depth == 0 {
                true
            } else if left == 0 {
                false
            } else {
                next_random(&mut seed) % 8 < open
            };
            if opens {
                s.push('(');
                left -= 1;
                depth += 1;
            } else {
                s.push(')');
                depth -= 1;
            }
        }
        chars += s.len();
        strings.push(s);
    }
    let mut kept = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for s in strings.iter() {
            let answer = remove_outer_parentheses(s);
            let n = answer.len() as i64;
            let middle = if n > 0 { answer.as_bytes()[(n / 2) as usize] as i64 } else { 0 };
            kept += n;
            check = (check * 31 + n * 2 + middle) % 1000000007;
        }
    }
    println!("{count} strings, {chars} characters, {rounds} rounds: {kept} kept, checksum {check}");
}
