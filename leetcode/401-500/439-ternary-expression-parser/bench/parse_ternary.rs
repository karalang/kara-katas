// Benchmark for #439: mirror of parse_ternary.kara (a stack, scanning
// from the right) on 200 random expressions of 2,499 ternaries each,
// built once and evaluated 20 times over.

fn parse_ternary(expression: &str) -> char {
    let e = expression.as_bytes();
    let mut stack: Vec<u8> = Vec::new();
    let mut i = e.len();
    while i > 0 {
        i -= 1;
        if !stack.is_empty() && stack[stack.len() - 1] == b'?' {
            stack.pop();
            let yes = stack.pop().expect("a yes value");
            stack.pop();
            let no = stack.pop().expect("a no value");
            stack.push(if e[i] == b'T' { yes } else { no });
        } else {
            stack.push(e[i]);
        }
    }
    stack[0] as char
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// Appends a random expression of exactly n ternaries to out: a random
// split of the n - 1 below the root between its two branches.
fn random_expression(seed: &mut i64, n: i64, out: &mut String) {
    if n == 0 {
        let r = next_random(seed) % 12;
        out.push(if r < 10 { (b'0' + r as u8) as char } else if r == 10 { 'T' } else { 'F' });
        return;
    }
    out.push(if next_random(seed) % 2 == 0 { 'T' } else { 'F' });
    out.push('?');
    let left = next_random(seed) % n;
    random_expression(seed, left, out);
    out.push(':');
    random_expression(seed, n - 1 - left, out);
}

fn main() {
    let count = 200;
    let ternaries = 2499;
    let rounds = 20;
    let mut seed: i64 = 439;
    let mut expressions: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut e = String::new();
        random_expression(&mut seed, ternaries, &mut e);
        expressions.push(e);
    }
    let mut digits = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for e in &expressions {
            let value = parse_ternary(e);
            if value != 'T' && value != 'F' {
                digits += 1;
            }
            checksum = (checksum * 31 + value as i64 + round) % 1000000007;
        }
    }
    println!(
        "{} expressions of {} characters, {} rounds: {} digits, checksum {}",
        count,
        expressions[0].len(),
        rounds,
        digits,
        checksum
    );
}
