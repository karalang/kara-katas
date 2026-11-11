// LeetCode #1111: Maximum Nesting Depth of Two Valid Parentheses Strings
// -- the bench in Rust: the ★ arm over the same 16 strings and the same
// valid prefixes.

fn max_depth_after_split(seq: &str) -> Vec<i32> {
    let mut depth = 0;
    let mut answer: Vec<i32> = Vec::with_capacity(seq.len());
    for c in seq.chars() {
        if c == '(' {
            answer.push(depth % 2);
            depth += 1;
        } else {
            depth -= 1;
            answer.push(depth % 2);
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_vps(seed: &mut i64, pairs: i64) -> (String, Vec<usize>) {
    let mut out = String::new();
    let mut cuts = Vec::new();
    let mut opens = 0;
    let mut depth = 0;
    while opens < pairs || depth > 0 {
        if opens < pairs && (depth == 0 || next_random(seed) % 2 == 0) {
            out.push('(');
            opens += 1;
            depth += 1;
        } else {
            out.push(')');
            depth -= 1;
            if depth == 0 {
                cuts.push(out.len());
            }
        }
    }
    (out, cuts)
}

fn main() {
    let mut seed = 1111;
    let strings: Vec<(String, Vec<usize>)> = (0..16).map(|_| random_vps(&mut seed, 5000)).collect();
    let mut chars: i64 = 0;
    let mut ones: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..1000usize {
        for j in 0..strings.len() {
            let (s, cuts) = &strings[j];
            let cut = cuts[(round * 7919 + j * 104729) % cuts.len()];
            let answer = max_depth_after_split(&s[0..cut]);
            chars += cut as i64;
            ones += answer.iter().map(|&g| g as i64).sum::<i64>();
            check = (check * 31 + answer[(round * 31 + j) % cut] as i64) % 1000000007;
        }
    }
    println!("1000 rounds over 16 strings of 10000 characters: {} characters, {} in the second group, checksum {}", chars, ones, check);
}
