// LeetCode #1736: Latest Time by Replacing Hidden Digits -- the bench
// (time.kara): each hidden digit the largest its neighbours allow.

fn maximum_time(time: &str) -> String {
    let mut t: Vec<char> = time.chars().collect();
    if t[0] == '?' {
        t[0] = if t[1] == '?' || t[1] <= '3' { '2' } else { '1' };
    }
    if t[1] == '?' {
        t[1] = if t[0] == '2' { '3' } else { '9' };
    }
    if t[3] == '?' {
        t[3] = '5';
    }
    if t[4] == '?' {
        t[4] = '9';
    }
    t.iter().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000000;
    let rounds: i64 = 10;
    let mut seed: i64 = 1736;
    let mut times: Vec<String> = Vec::new();
    for _ in 0..count {
        let t = next_random(&mut seed) % 1440;
        let shown = format!(
            "{}{}:{}{}",
            t / 60 / 10,
            t / 60 % 10,
            t % 60 / 10,
            t % 60 % 10
        );
        let mut hidden = String::new();
        for c in shown.chars() {
            if c != ':' && next_random(&mut seed) % 2 == 0 {
                hidden.push('?');
            } else {
                hidden.push(c);
            }
        }
        times.push(hidden);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for time in times.iter() {
            let answer = maximum_time(time);
            let b = answer.as_bytes();
            sum += b[1] as i64 - 48;
            check = (check * 31
                + b[0] as i64 * 1000
                + b[1] as i64 * 100
                + b[3] as i64 * 10
                + b[4] as i64
                + r)
                % 1000000007;
        }
    }
    println!(
        "{} times, {} rounds: hour digits sum to {}, checksum {}",
        count, rounds, sum, check
    );
}
