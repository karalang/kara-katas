// LeetCode #1614: Maximum Nesting Depth of the Parentheses -- the bench in
// Rust, mirroring depth.kara: one pass over `chars()` counting the
// parentheses open, keeping the most.

fn max_depth(s: &str) -> i32 {
    let mut open = 0;
    let mut most = 0;
    for c in s.chars() {
        if c == '(' {
            open += 1;
            most = most.max(open);
        } else if c == ')' {
            open -= 1;
        }
    }
    most
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn expression(size: i64, out: &mut String, seed: &mut i64) {
    let mut left = size;
    loop {
        if left > 1 && next_random(seed) % 3 == 0 {
            let inner = next_random(seed) % left + 1;
            out.push('(');
            expression(inner, out, seed);
            out.push(')');
            left -= inner;
        } else {
            out.push((b'0' + (next_random(seed) % 10) as u8) as char);
            left -= 1;
        }
        if left <= 0 {
            break;
        }
        out.push(['+', '-', '*', '/'][(next_random(seed) % 4) as usize]);
    }
}

fn main() {
    let mut seed: i64 = 1614;
    let mut expressions = Vec::new();
    for _ in 0..10 {
        let mut s = String::new();
        expression(200000, &mut s, &mut seed);
        expressions.push(s);
    }
    let mut check: i64 = 0;
    let mut chars = 0;
    for s in &expressions {
        for _ in 0..10 {
            check = (check * 31 + max_depth(s) as i64 + 1) % 1000000007;
            chars += s.len();
        }
    }
    println!("10 expressions of 200000 terms, each read 10 times: {chars} characters, checksum {check}");
}
