// Benchmark: LeetCode #1087 Brace Expansion -- mirrors brace_expansion.kara:
// the pattern read into sorted groups and the words built by a depth-first
// walk, over 2000 patterns built once.

fn groups_of(s: &str) -> Vec<Vec<char>> {
    let mut groups: Vec<Vec<char>> = Vec::new();
    let mut open: Option<Vec<char>> = None;
    for c in s.chars() {
        match c {
            '{' => open = Some(Vec::new()),
            '}' => {
                let mut g = open.take().unwrap();
                g.sort();
                groups.push(g);
            }
            ',' => {}
            _ => match open {
                Some(ref mut g) => g.push(c),
                None => groups.push(vec![c]),
            },
        }
    }
    groups
}

fn walk(groups: &Vec<Vec<char>>, at: usize, word: &mut String, out: &mut Vec<String>) {
    if at == groups.len() {
        out.push(word.clone());
        return;
    }
    for &c in groups[at].iter() {
        word.push(c);
        walk(groups, at + 1, word, out);
        word.pop();
    }
}

fn expand(s: &str) -> Vec<String> {
    let groups = groups_of(s);
    let mut word = String::new();
    let mut out: Vec<String> = Vec::new();
    walk(&groups, 0, &mut word, &mut out);
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_pattern(seed: &mut i64, most: usize, k: i64) -> String {
    let mut s = String::new();
    let parts = next_random(seed) % 8 + 1;
    for _ in 0..parts {
        if next_random(seed) % 2 == 0 {
            let c = (b'a' + (next_random(seed) % k) as u8) as char;
            if s.len() + 1 <= most {
                s.push(c);
            }
        } else {
            let want = (next_random(seed) % k + 1) as usize;
            let mut letters: Vec<char> = Vec::new();
            while letters.len() < want {
                let c = (b'a' + (next_random(seed) % k) as u8) as char;
                if !letters.contains(&c) {
                    letters.push(c);
                }
            }
            let parts: Vec<String> = letters.iter().map(|c| c.to_string()).collect();
            let group = format!("{{{}}}", parts.join(","));
            if s.len() + group.len() <= most {
                s.push_str(&group);
            }
        }
    }
    if s.is_empty() {
        s.push('a');
    }
    s
}

fn main() {
    let rounds: i64 = 400;
    let mut seed = 1087;
    let mut patterns: Vec<String> = Vec::new();
    for t in 0..2000 {
        patterns.push(random_pattern(&mut seed, 50, t % 6 + 1));
    }
    let mut words: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..2000 {
            let out = expand(&patterns[((r * 7 + i) % 2000) as usize]);
            words += out.len() as i64;
            let mid = out[out.len() / 2].as_bytes();
            check = (check * 31 + out.len() as i64 + mid[mid.len() - 1] as i64) % 1000000007;
        }
    }
    println!("{} rounds over 2000 patterns: {} words, checksum {}", rounds, words, check);
}
