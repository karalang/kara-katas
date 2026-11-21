// LeetCode #2483: Minimum Penalty for a Shop -- bench, Rust mirror of
// shop.kara.

fn best_closing_time(customers: &str) -> i64 {
    let mut balance = 0;
    let mut best = 0;
    let mut best_hour = 0;
    let mut hour = 0;
    for c in customers.chars() {
        if c == 'Y' {
            balance += 1;
        } else {
            balance -= 1;
        }
        hour += 1;
        if balance > best {
            best = balance;
            best_hour = hour;
        }
    }
    best_hour
}

fn main() {
    let mut seed: i64 = 2483;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut logs: Vec<Vec<char>> = (0..20).map(|_| (0..10000).map(|_| if next_random() % 2 == 0 { 'Y' } else { 'N' }).collect()).collect();
    let mut check: i64 = 0;
    for p in 0..600 {
        for g in 0..20 {
            let at = (check % 10000) as usize;
            logs[g][at] = if logs[g][at] == 'Y' { 'N' } else { 'Y' };
            let log: String = logs[g].iter().collect();
            check = (check * 31 + best_closing_time(&log) + p) % 1000000007;
        }
    }
    println!("600 passes over 20 logs of 10^4 hours: checksum {}", check);
}
