// Benchmark for #591: Rust mirror of the ★ arm (one scan with a stack of
// open tags); see tag_validator.kara. The stack holds owned `String`s,
// as the Kāra arm's does.

fn valid_name(name: &str) -> bool {
    name.len() >= 1 && name.len() <= 9 && name.chars().all(|c| c >= 'A' && c <= 'Z')
}

fn is_valid(code: &str) -> bool {
    let n = code.len();
    let mut stack: Vec<String> = Vec::new();
    let mut i = 0;
    while i < n {
        if i > 0 && stack.is_empty() {
            return false;
        }
        if code[i..].starts_with("<![CDATA[") {
            if stack.is_empty() {
                return false;
            }
            match code[i + 9..].find("]]>") {
                Some(k) => i += 9 + k + 3,
                None => return false,
            }
        } else if code[i..].starts_with("</") {
            let start = i + 2;
            let Some(k) = code[start..].find('>') else {
                return false;
            };
            let name = &code[start..start + k];
            if stack.is_empty() || stack[stack.len() - 1] != name {
                return false;
            }
            stack.pop();
            i = start + k + 1;
        } else if code[i..].starts_with('<') {
            let start = i + 1;
            let Some(k) = code[start..].find('>') else {
                return false;
            };
            let name = &code[start..start + k];
            if !valid_name(name) {
                return false;
            }
            stack.push(name.to_string());
            i = start + k + 1;
        } else {
            if stack.is_empty() {
                return false;
            }
            i += 1;
        }
    }
    stack.is_empty()
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn snippet(depth: i64, seed: &mut i64) -> String {
    let names = ["A", "XY", "ABCDEFGHI", "CODE"];
    let texts = ["x", " ", ">", "]]>", "!", "[", "y", "/", "...", "<![CDATA[<A>]]>"];
    let name = names[(step(seed) % names.len() as i64) as usize];
    let mut out = format!("<{}>", name);
    let parts = step(seed) % 7;
    for _ in 0..parts {
        if step(seed) % 10 < 4 && depth > 0 {
            out.push_str(&snippet(depth - 1, seed));
        } else {
            out.push_str(texts[(step(seed) % texts.len() as i64) as usize]);
        }
    }
    if step(seed) % 40 == 0 {
        out.push_str("</B>");
    } else {
        out.push_str(&format!("</{}>", name));
    }
    out
}

fn main() {
    let count = 1000;
    let rounds = 1000;
    let mut seed: i64 = 591;
    let mut codes: Vec<String> = Vec::new();
    while codes.len() < count {
        let code = snippet(4, &mut seed);
        if code.len() >= 200 && code.len() <= 500 {
            codes.push(code);
        }
    }
    let mut valid = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            if is_valid(&codes[(round * 7 + g) % count]) {
                valid += 1;
                checksum = (checksum * 31 + g as i64 + 1) % 1000000007;
            }
        }
    }
    println!("{} snippets, {} rounds: {} valid, checksum {}", count, rounds, valid, checksum);
}
