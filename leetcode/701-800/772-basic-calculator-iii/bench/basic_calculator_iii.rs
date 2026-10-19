// LeetCode 772 — Basic Calculator III: benchmark, the ★ arm in Rust.
// Sixty-four random expressions of 2,400 numbers, up to LeetCode's limit
// of 10,000 characters, built once; ROUNDS rounds each evaluate the next.
// At each operator the generator takes the first, from a random start,
// that keeps every value valid: no division by zero, nothing beyond 32
// bits.

const ROUNDS: i64 = 6000;
const LEAVES: i64 = 2400;

struct Cursor<'a> {
    bytes: &'a [u8],
    at: usize,
}

impl Cursor<'_> {
    fn peek(&self) -> u8 {
        if self.at < self.bytes.len() { self.bytes[self.at] } else { 0 }
    }

    fn sum(&mut self) -> i64 {
        let mut value = self.term();
        loop {
            let op = self.peek();
            if op != b'+' && op != b'-' {
                return value;
            }
            self.at += 1;
            let right = self.term();
            value = if op == b'+' { value + right } else { value - right };
        }
    }

    fn term(&mut self) -> i64 {
        let mut value = self.factor();
        loop {
            let op = self.peek();
            if op != b'*' && op != b'/' {
                return value;
            }
            self.at += 1;
            let right = self.factor();
            value = if op == b'*' { value * right } else { value / right };
        }
    }

    fn factor(&mut self) -> i64 {
        if self.peek() == b'(' {
            self.at += 1;
            let value = self.sum();
            self.at += 1;
            return value;
        }
        let mut value = 0;
        while self.peek().is_ascii_digit() {
            value = value * 10 + (self.peek() - b'0') as i64;
            self.at += 1;
        }
        value
    }
}

fn calculate(s: &str) -> i64 {
    let mut cursor = Cursor { bytes: s.as_bytes(), at: 0 };
    cursor.sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn combine(a: i64, op: u8, b: i64) -> Option<i64> {
    if op == b'/' && b == 0 {
        return None;
    }
    let value = match op {
        b'+' => a + b,
        b'-' => a - b,
        b'*' => a * b,
        _ => a / b,
    };
    if value < -2147483648 || value > 2147483647 { None } else { Some(value) }
}

struct Piece {
    text: String,
    value: i64,
    level: i64,
}

fn build(seed: &mut i64, leaves: i64) -> Piece {
    if leaves == 1 {
        let n = if next_random(seed) % 4 == 0 { next_random(seed) % 1000 } else { next_random(seed) % 10 };
        return Piece { text: n.to_string(), value: n, level: 3 };
    }
    let left_leaves = 1 + next_random(seed) % (leaves - 1);
    let left = build(seed, left_leaves);
    let right = build(seed, leaves - left_leaves);
    let ops = b"+-*/";
    let mut k = (next_random(seed) % 4) as usize;
    while combine(left.value, ops[k], right.value).is_none() {
        k = (k + 1) % 4;
    }
    let op = ops[k];
    let value = combine(left.value, op, right.value).unwrap();
    let level = if op == b'+' || op == b'-' { 1 } else { 2 };
    let left_text = if left.level < level || next_random(seed) % 4 == 0 { format!("({})", left.text) } else { left.text.clone() };
    let right_text = if right.level < level || (right.level == level && op != b'+') || next_random(seed) % 4 == 0 {
        format!("({})", right.text)
    } else {
        right.text.clone()
    };
    Piece { text: format!("{}{}{}", left_text, op as char, right_text), value, level }
}

fn main() {
    let mut seed = 772;
    let mut pool: Vec<String> = Vec::new();
    let mut longest = 0;
    for _ in 0..64 {
        let piece = build(&mut seed, LEAVES);
        longest = longest.max(piece.text.len());
        pool.push(piece.text);
    }
    let mut check: i64 = 0;
    for round in 0..ROUNDS {
        let value = calculate(&pool[(round % 64) as usize]);
        check = ((check * 31 + value) % 1000000007 + 1000000007) % 1000000007;
    }
    println!("{ROUNDS} expressions of up to {longest} characters: checksum {check}");
}
