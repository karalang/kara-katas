// LeetCode #2468: Split Message Based on Limit -- the bench, the ★ arm in
// Rust: the least part count found with a running sum of the counts'
// digits, each count's digits by `to_string`, then the parts cut in order
// by `format!`.

fn digits(v: i64) -> i64 {
    v.to_string().len() as i64
}

fn split_message(message: &str, limit: i64) -> Vec<String> {
    let n = message.len() as i64;
    let mut digit_sum = 0;
    let mut parts = 0;
    let mut b = 1;
    while 3 + 2 * digits(b) < limit {
        digit_sum += digits(b);
        if b * (limit - 3 - digits(b)) - digit_sum >= n {
            parts = b;
            break;
        }
        b += 1;
    }
    let mut out = Vec::new();
    if parts == 0 {
        return out;
    }
    let mut at = 0;
    for a in 1..parts + 1 {
        let room = limit - 3 - digits(a) - digits(parts);
        let end = (at + room).min(n);
        out.push(format!("{}<{}/{}>", &message[at as usize..end as usize], a, parts));
        at = end;
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 messages of 10^4 lowercase letters and spaces built once; then
    // 2600 passes, each choosing every message's limit, from 12 to 211,
    // from the checksum so far, then splitting it and folding the part
    // count, the last part's length and the pass into the checksum
    let mut seed = 2468;
    let letters = b"abcdefghijklmnopqrstuvwxyz ";
    let mut messages: Vec<String> = Vec::new();
    for _ in 0..20 {
        let mut text = String::new();
        for _ in 0..10000 {
            text.push(letters[(next_random(&mut seed) % 27) as usize] as char);
        }
        messages.push(text);
    }
    let mut check = 0i64;
    for p in 0..2600i64 {
        for m in &messages {
            let limit = 12 + check % 200;
            let parts = split_message(m, limit);
            let last = parts[parts.len() - 1].len() as i64;
            check = (check * 31 + parts.len() as i64 + last + p) % 1000000007;
        }
    }
    println!("2600 passes over 20 messages of 10^4: checksum {}", check);
}
