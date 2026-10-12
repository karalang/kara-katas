// Benchmark for #388: mirror of length_longest_path.kara (path lengths by depth).

fn length_longest_path(input: &str) -> i64 {
    let b = input.as_bytes();
    let mut len: Vec<i64> = vec![0];
    let mut best = 0;
    let mut i = 0;
    while i < b.len() {
        let mut depth = 0;
        while i < b.len() && b[i] == b'\t' {
            depth += 1;
            i += 1;
        }
        let start = i;
        let mut is_file = false;
        while i < b.len() && b[i] != b'\n' {
            if b[i] == b'.' {
                is_file = true;
            }
            i += 1;
        }
        let path = len[depth] + (i - start) as i64;
        if is_file {
            if path > best {
                best = path;
            }
        } else if depth + 1 < len.len() {
            len[depth + 1] = path + 1;
        } else {
            len.push(path + 1);
        }
        i += 1;
    }
    best
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn listing(seed: &mut i64, entries: i64) -> String {
    let mut out = String::new();
    let (mut open, mut depth) = (0i64, 0i64);
    for k in 0..entries {
        let r = step(seed) % 100;
        if r < 35 {
            depth = open;
        } else if r >= 70 {
            let up = (r - 70) / 10 + 1;
            depth = if up > depth { 0 } else { depth - up };
        }
        if depth > open {
            depth = open;
        }
        let name_len = step(seed) % 12 + 1;
        let file = step(seed) % 3 == 0;
        if k > 0 {
            out.push('\n');
        }
        for _ in 0..depth {
            out.push('\t');
        }
        for _ in 0..name_len {
            out.push((step(seed) % 26 + 97) as u8 as char);
        }
        if file {
            out.push_str(".ext");
            open = depth;
        } else {
            open = if depth < 6 { depth + 1 } else { depth };
        }
    }
    out
}

fn main() {
    let mut seed: i64 = 388;
    let mut listings: Vec<String> = Vec::new();
    let mut bytes = 0;
    for _ in 0..200 {
        let s = listing(&mut seed, 800);
        bytes += s.len();
        listings.push(s);
    }
    let mut checksum: i64 = 0;
    for round in 0..150i64 {
        for s in &listings {
            let r = length_longest_path(s);
            checksum = (checksum * 31 + r + round) % 1000000007;
        }
    }
    println!("{} bytes in 200 listings, 150 rounds, checksum {}", bytes, checksum);
}
