// LeetCode #2284: Sender With Largest Word Count -- the bench, the ★
// arm's Rust twin. A `HashMap` of totals, then the largest by total and
// name.
use std::collections::HashMap;

fn largest_word_count(messages: &[String], senders: &[String]) -> String {
    let mut totals: HashMap<String, i64> = HashMap::new();
    for (message, sender) in messages.iter().zip(senders.iter()) {
        let words = message.split(' ').count() as i64;
        *totals.entry(sender.clone()).or_insert(0) += words;
    }
    let mut best = String::new();
    let mut most = 0;
    for (sender, &total) in totals.iter() {
        if total > most || (total == most && *sender > best) {
            best = sender.clone();
            most = total;
        }
    }
    best
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(len: i64, seed: &mut i64) -> String {
    let mut w = String::new();
    for _ in 0..len {
        w.push((b'a' + (next_random(seed) % 26) as u8) as char);
    }
    w
}

fn main() {
    let mut seed: i64 = 2284;
    let mut pool: Vec<String> = Vec::new();
    for _ in 0..40 {
        let len = next_random(&mut seed) % 10 + 1;
        pool.push(word(len, &mut seed));
    }
    let mut cases: Vec<(Vec<String>, Vec<String>)> = Vec::new();
    for _ in 0..1000 {
        let first = next_random(&mut seed) % 20;
        let mut messages: Vec<String> = Vec::new();
        let mut senders: Vec<String> = Vec::new();
        for _ in 0..100 {
            senders.push(pool[(first + next_random(&mut seed) % 20) as usize].clone());
            let w = next_random(&mut seed) % 8 + 1;
            let mut message = String::new();
            for j in 0..w {
                if j > 0 {
                    message.push(' ');
                }
                let len = next_random(&mut seed) % 5 + 1;
                message.push_str(&word(len, &mut seed));
            }
            messages.push(message);
        }
        cases.push((messages, senders));
    }
    let mut check: i64 = 0;
    for _ in 0..20 {
        for (messages, senders) in cases.iter() {
            let best = largest_word_count(messages, senders);
            let sum: i64 = best.bytes().map(|b| b as i64).sum();
            check = (check * 31 + sum) % 1000000007;
        }
    }
    println!("20 passes over 1000 cases of 100 messages: checksum {}", check);
}
