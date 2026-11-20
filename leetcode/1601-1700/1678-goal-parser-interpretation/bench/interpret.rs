// LeetCode #1678: Goal Parser Interpretation -- the bench's Rust mirror:
// the ★ arm on 100000 random commands of up to 100 characters, all drawn
// first, each interpreted 20 times.

fn interpret(command: &str) -> String {
    let bytes = command.as_bytes();
    let mut out = String::with_capacity(command.len());
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i] == b'G' {
            out.push('G');
            i += 1;
        } else if bytes[i + 1] == b')' {
            out.push('o');
            i += 2;
        } else {
            out.push_str("al");
            i += 4;
        }
    }
    out
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds: i64 = 20;
    let tokens = ["G", "()", "(al)"];
    let mut seed: i64 = 1678;
    let mut commands: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut command = String::new();
        let length = (next_random(&mut seed) % 100 + 1) as usize;
        loop {
            let token = tokens[(next_random(&mut seed) % 3) as usize];
            if command.len() + token.len() > length {
                break;
            }
            command.push_str(token);
        }
        if command.is_empty() {
            command.push('G');
        }
        commands.push(command);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for command in &commands {
            let answer = interpret(command);
            let n = answer.len() as i64;
            total += n;
            check = (check * 31 + n + answer.as_bytes()[answer.len() - 1] as i64 + r) % 1000000007;
        }
    }
    println!("{} commands, {} rounds: {} letters, checksum {}", count, rounds, total, check);
}
