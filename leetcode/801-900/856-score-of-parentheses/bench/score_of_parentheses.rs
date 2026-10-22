// Benchmark for #856: Score of Parentheses -- the ★ arm, mirroring
// score_of_parentheses.kara.

fn score_of_parentheses(s: &str) -> i64 {
    let mut stack: Vec<i64> = vec![0];
    for c in s.chars() {
        if c == '(' {
            stack.push(0);
        } else {
            let inner = stack.pop().unwrap();
            let worth = if inner == 0 { 1 } else { 2 * inner };
            let top = stack.len() - 1;
            stack[top] += worth;
        }
    }
    stack[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let rounds = 4000000;
    let mut seed: i64 = 856;
    let mut strings: Vec<String> = Vec::new();
    for g in 0..count {
        let mut s = String::new();
        let mut opens = 0;
        let mut balance = 0;
        while s.len() < 50 {
            if opens < 25 && (balance == 0 || next_random(&mut seed) % 4 < 1 + g % 3) {
                s.push('(');
                opens += 1;
                balance += 1;
            } else {
                s.push(')');
                balance -= 1;
            }
        }
        strings.push(s);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let k = score_of_parentheses(&strings[round % count as usize]);
        total += k;
        checksum = (checksum * 31 + k) % 1000000007;
    }
    println!("{} rounds of 64 strings: scores sum to {}, checksum {}", rounds, total, checksum);
}
