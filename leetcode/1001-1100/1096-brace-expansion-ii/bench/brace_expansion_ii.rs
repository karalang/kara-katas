// Benchmark: LeetCode #1096 Brace Expansion II -- Rust mirror of
// brace_expansion_ii.kara: the stack arm, two Vec<String>s sorted and
// deduplicated at each `}`, over 64 expressions of up to 60 characters
// built once, each round changing one letter in every expression.

fn join(words: &[String], part: &[String]) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    for a in words.iter() {
        for b in part.iter() {
            out.push(a.clone() + b);
        }
    }
    out
}

fn brace_expansion_ii(expression: &str) -> Vec<String> {
    let mut stack: Vec<(Vec<String>, Vec<String>)> = Vec::new();
    let mut union: Vec<String> = Vec::new();
    let mut concat: Vec<String> = vec![String::new()];
    for c in expression.chars() {
        match c {
            '{' => {
                stack.push((union, concat));
                union = Vec::new();
                concat = vec![String::new()];
            }
            ',' => {
                union.extend(concat);
                concat = vec![String::new()];
            }
            '}' => {
                union.extend(concat);
                union.sort();
                union.dedup();
                let (outer_union, outer_concat) = stack.pop().unwrap();
                concat = join(&outer_concat, &union);
                union = outer_union;
            }
            _ => concat = join(&concat, &[c.to_string()]),
        }
    }
    union.extend(concat);
    union.sort();
    union.dedup();
    union
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(seed: &mut i64) -> char {
    (b'a' + (next_random(seed) % 6) as u8) as char
}

fn option(seed: &mut i64) -> String {
    let mut s = String::new();
    if next_random(seed) % 4 == 0 {
        s.push('{');
        s.push(letter(seed));
        s.push(',');
        s.push(letter(seed));
        s.push('}');
        s.push(letter(seed));
    } else {
        for _ in 0..next_random(seed) % 2 + 1 {
            s.push(letter(seed));
        }
    }
    s
}

fn main() {
    let mut seed: i64 = 1096;
    let mut expressions: Vec<Vec<char>> = Vec::new();
    while expressions.len() < 64 {
        let mut s = String::new();
        for _ in 0..5 {
            let options: Vec<String> = (0..next_random(&mut seed) % 2 + 2).map(|_| option(&mut seed)).collect();
            s.push_str(&format!("{{{}}}", options.join(",")));
        }
        if s.len() <= 60 {
            expressions.push(s.chars().collect());
        }
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..200i64 {
        for j in 0..expressions.len() {
            let e = &mut expressions[j];
            let at = ((round * 7 + j as i64 * 13) % e.len() as i64) as usize;
            if e[at].is_ascii_lowercase() {
                e[at] = (b'a' + ((round + j as i64) % 6) as u8) as char;
            }
            let text: String = e.iter().collect();
            let words = brace_expansion_ii(&text);
            total += words.len() as i64;
            check = (check * 31 + words.len() as i64) % 1000000007;
            for b in words[0].bytes().chain(words[words.len() - 1].bytes()) {
                check = (check * 131 + b as i64) % 1000000007;
            }
        }
    }
    println!("200 rounds over 64 expressions: {} words, checksum {}", total, check);
}
