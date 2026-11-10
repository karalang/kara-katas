// LeetCode #1106: Parsing A Boolean Expression -- the bench in Rust: the
// ★ arm (recursive descent from a shared position) over 32 expressions of
// up to about 2 * 10^4 characters, each round flipping one value in every
// expression and parsing it again.

fn parse(s: &[char], at: &mut usize) -> bool {
    let c = s[*at];
    *at += 1;
    match c {
        't' => true,
        'f' => false,
        _ => {
            *at += 1;
            let mut values: Vec<bool> = Vec::new();
            loop {
                values.push(parse(s, at));
                let next = s[*at];
                *at += 1;
                if next == ')' {
                    break;
                }
            }
            match c {
                '!' => !values[0],
                '&' => values.iter().all(|&v| v),
                _ => values.iter().any(|&v| v),
            }
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_expr(seed: &mut i64, out: &mut Vec<char>, budget: i64, depth: i64) {
    if budget <= 1 || depth == 0 {
        out.push(if next_random(seed) % 2 == 0 { 't' } else { 'f' });
        return;
    }
    let op = next_random(seed) % 3;
    if op == 0 {
        out.push('!');
        out.push('(');
        random_expr(seed, out, budget - 1, depth - 1);
        out.push(')');
        return;
    }
    let k = next_random(seed) % 4 + 1;
    out.push(if op == 1 { '&' } else { '|' });
    out.push('(');
    for i in 0..k {
        if i > 0 {
            out.push(',');
        }
        random_expr(seed, out, (budget - 1) / k, depth - 1);
    }
    out.push(')');
}

fn main() {
    let mut seed = 1106;
    let mut cases: Vec<Vec<char>> = Vec::new();
    let mut values: Vec<Vec<usize>> = Vec::new();
    let mut length = 0;
    for _ in 0..32 {
        let mut e: Vec<char> = Vec::new();
        random_expr(&mut seed, &mut e, 6000, 20);
        let at: Vec<usize> = (0..e.len()).filter(|&i| e[i] == 't' || e[i] == 'f').collect();
        length += e.len();
        cases.push(e);
        values.push(at);
    }
    let mut trues = 0;
    let mut check: i64 = 0;
    for round in 0..200usize {
        for j in 0..cases.len() {
            let i = values[j][(round * 7919 + j * 104729) % values[j].len()];
            cases[j][i] = if cases[j][i] == 't' { 'f' } else { 't' };
            let mut at = 0;
            let v = parse(&cases[j], &mut at);
            if v {
                trues += 1;
            }
            check = (check * 31 + if v { 2 } else { 1 }) % 1000000007;
        }
    }
    println!("200 rounds over 32 expressions of {} characters: {} true, checksum {}", length, trues, check);
}
