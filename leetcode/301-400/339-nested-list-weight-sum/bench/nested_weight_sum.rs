// Benchmark mirror of nested_weight_sum.kara (LeetCode #339): parse a list's
// text into the tree, then walk it. Same lists, rounds and sink.

enum Nested {
    Int(i64),
    List(Vec<Nested>),
}

fn depth_sum(items: &Vec<Nested>, depth: i64) -> i64 {
    let mut total = 0;
    for item in items.iter() {
        match item {
            Nested::Int(v) => total += v * depth,
            Nested::List(inner) => total += depth_sum(inner, depth + 1),
        }
    }
    total
}

fn weight_sum(items: &Vec<Nested>) -> i64 {
    depth_sum(items, 1)
}

fn parse_list(text: &Vec<char>, pos: &mut usize) -> Vec<Nested> {
    let mut items: Vec<Nested> = Vec::new();
    *pos += 1;
    while text[*pos] != ']' {
        if text[*pos] == ',' {
            *pos += 1;
        } else if text[*pos] == '[' {
            items.push(Nested::List(parse_list(text, pos)));
        } else {
            let mut sign = 1;
            if text[*pos] == '-' {
                sign = -1;
                *pos += 1;
            }
            let mut v: i64 = 0;
            while text[*pos].is_ascii_digit() {
                v = v * 10 + (text[*pos] as i64 - '0' as i64);
                *pos += 1;
            }
            items.push(Nested::Int(sign * v));
        }
    }
    *pos += 1;
    items
}

fn parse(text: &String) -> Vec<Nested> {
    let cs: Vec<char> = text.chars().collect();
    let mut pos = 0;
    parse_list(&cs, &mut pos)
}

fn next(state: &mut i64) -> i64 {
    *state = (*state * 1103515245 + 12345) % 2147483648;
    *state >> 8
}

fn gen_member(state: &mut i64, depth: i64, max_depth: i64, out: &mut String) {
    if depth < max_depth && next(state) % 3 == 0 {
        out.push('[');
        let count = next(state) % 5;
        for k in 0..count {
            if k > 0 {
                out.push(',');
            }
            gen_member(state, depth + 1, max_depth, out);
        }
        out.push(']');
    } else {
        let v = next(state) % 201 - 100;
        out.push_str(&v.to_string());
    }
}

fn gen_text(seed: i64, top: i64, max_depth: i64) -> String {
    let mut state = seed;
    let mut out = String::new();
    out.push('[');
    for k in 0..top {
        if k > 0 {
            out.push(',');
        }
        gen_member(&mut state, 1, max_depth, &mut out);
    }
    out.push(']');
    out
}

fn main() {
    let mut texts: Vec<String> = Vec::new();
    for s in 0..8 {
        texts.push(gen_text(s * 7919 + 1, 800, 12));
    }
    let mut hash: i64 = 0;
    for r in 0..4000 {
        let items = parse(&texts[r % 8]);
        let w = weight_sum(&items);
        hash = (hash * 31 + w + 1000000) % 1000000007;
    }
    println!("{}", hash);
}
