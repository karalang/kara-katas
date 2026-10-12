// Benchmark for #385: mirror of mini_parser.kara (recursive descent).

enum NestedInteger {
    Int(i64),
    List(Vec<NestedInteger>),
}

fn deserialize(s: &str) -> NestedInteger {
    let b = s.as_bytes();
    let mut pos = 0usize;
    parse_value(b, &mut pos)
}

fn parse_value(b: &[u8], pos: &mut usize) -> NestedInteger {
    if b[*pos] == b'[' {
        *pos += 1;
        let mut items: Vec<NestedInteger> = Vec::new();
        if b[*pos] == b']' {
            *pos += 1;
            return NestedInteger::List(items);
        }
        loop {
            items.push(parse_value(b, pos));
            if b[*pos] == b',' {
                *pos += 1;
            } else {
                *pos += 1;
                return NestedInteger::List(items);
            }
        }
    }
    let mut negative = false;
    if b[*pos] == b'-' {
        negative = true;
        *pos += 1;
    }
    let mut n: i64 = 0;
    while *pos < b.len() && b[*pos].is_ascii_digit() {
        n = n * 10 + (b[*pos] - b'0') as i64;
        *pos += 1;
    }
    NestedInteger::Int(if negative { -n } else { n })
}

fn shape(x: &NestedInteger) -> (i64, i64, i64) {
    match x {
        NestedInteger::Int(n) => (0, 1, *n),
        NestedInteger::List(items) => {
            let (mut depth, mut count, mut sum) = (0, 0, 0);
            for item in items {
                let (d, c, s) = shape(item);
                depth = depth.max(d);
                count += c;
                sum += s;
            }
            (depth + 1, count, sum)
        }
    }
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64, depth: i64) -> String {
    let r = next(seed) % 10;
    if depth == 0 || r < 4 {
        return format!("{}", next(seed) % 2000001 - 1000000);
    }
    let n = next(seed) % 5;
    let mut out = String::from("[");
    for i in 0..n {
        if i > 0 {
            out.push(',');
        }
        out.push_str(&random_value(seed, depth - 1));
    }
    out.push(']');
    out
}

fn main() {
    let mut seed: i64 = 385;
    let mut s = String::from("[");
    while s.len() < 49000 {
        if s.len() > 1 {
            s.push(',');
        }
        s.push_str(&random_value(&mut seed, 5));
    }
    s.push(']');
    let p = 1000000007i64;
    let mut checksum: i64 = 0;
    for _ in 0..2000 {
        let x = deserialize(&s);
        let (depth, count, sum) = shape(&x);
        checksum = ((checksum * 31 + depth * 7 + count) % p + sum % p + p) % p;
    }
    println!("{} bytes parsed 2000 times, checksum {}", s.len(), checksum);
}
