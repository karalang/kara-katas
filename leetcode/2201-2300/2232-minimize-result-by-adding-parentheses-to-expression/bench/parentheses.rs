// LeetCode #2232: Minimize Result by Adding Parentheses to Expression --
// the benchmark's Rust mirror of parentheses.kara: every place for the
// two parentheses, the first smallest a * (b + c) * d kept.

fn minimize_result(expression: &str) -> String {
    let plus = expression.find('+').unwrap();
    let left = &expression[..plus];
    let right = &expression[plus + 1..];
    let mut best = i64::MAX;
    let mut answer = String::new();
    for i in 0..left.len() {
        for j in 1..=right.len() {
            let a = if i == 0 { 1 } else { left[..i].parse::<i64>().unwrap() };
            let b = left[i..].parse::<i64>().unwrap();
            let c = right[..j].parse::<i64>().unwrap();
            let d = if j == right.len() { 1 } else { right[j..].parse::<i64>().unwrap() };
            let value = a * (b + c) * d;
            if value < best {
                best = value;
                answer = format!("{}({}+{}){}", &left[..i], &left[i..], &right[..j], &right[j..]);
            }
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw_expression(seed: &mut i64) -> String {
    let left = next_random(seed) % 8 + 1;
    let right = next_random(seed) % (9 - left) + 1;
    let mut expression = String::new();
    for k in 0..left + right + 1 {
        if k == left {
            expression.push('+');
        } else {
            expression.push((49 + next_random(seed) % 9) as u8 as char);
        }
    }
    expression
}

fn main() {
    let mut seed = 2232;
    let mut expressions: Vec<String> = (0..20000).map(|_| draw_expression(&mut seed)).collect();
    let mut check: i64 = 0;
    for _ in 0..20 {
        // punch: one expression drawn again before each pass over all
        let at = (next_random(&mut seed) % 20000) as usize;
        expressions[at] = draw_expression(&mut seed);
        for expression in &expressions {
            let answer = minimize_result(expression);
            check = (check * 31 + answer.len() as i64 + answer.find('(').unwrap() as i64 * 11 + answer.find(')').unwrap() as i64) % 1000000007;
        }
    }
    println!("20 passes over 20000 expressions: checksum {check}");
}
