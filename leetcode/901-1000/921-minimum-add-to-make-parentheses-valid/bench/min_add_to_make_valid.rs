// LeetCode #921: Minimum Add to Make Parentheses Valid -- bench: one count
// of the open parentheses. Mirrors min_add_to_make_valid.kara.

fn min_add_to_make_valid(s: &str) -> i64 {
    let mut open = 0;
    let mut added = 0;
    for c in s.bytes() {
        if c == b'(' {
            open += 1;
        } else if open > 0 {
            open -= 1;
        } else {
            added += 1;
        }
    }
    added + open
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n) = (100, 1000, 1000);
    let mut seed = 921;
    // count strings of n parentheses, built once, leaning from ')' to '('
    let mut strings: Vec<String> = Vec::new();
    for i in 0..count {
        let lean = 30 + i as i64 % 41;
        let s: String = (0..n).map(|_| if next_random(&mut seed) % 100 < lean { '(' } else { ')' }).collect();
        strings.push(s);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round visits every string, starting from a different one
        for i in 0..count {
            let a = min_add_to_make_valid(&strings[(r + i) % count]);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} strings of {n}: answers summing to {total}, checksum {check}");
}
