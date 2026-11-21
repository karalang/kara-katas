// LeetCode #2409: Count Days Spent Together -- the bench, the ★ arm in
// Rust: each "MM-DD" read from its bytes into a day of the year, the
// shared stay from the later arrival to the earlier departure.

const BEFORE: [i64; 12] = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];

fn day_of_year(date: &str) -> i64 {
    let b = date.as_bytes();
    let month = ((b[0] - b'0') * 10 + b[1] - b'0') as usize;
    let day = ((b[3] - b'0') * 10 + b[4] - b'0') as i64;
    BEFORE[month - 1] + day
}

fn count_days_together(arrive_alice: &str, leave_alice: &str, arrive_bob: &str, leave_bob: &str) -> i64 {
    let first = day_of_year(arrive_alice).max(day_of_year(arrive_bob));
    let last = day_of_year(leave_alice).min(day_of_year(leave_bob));
    (last - first + 1).max(0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    let mut names: Vec<String> = Vec::new();
    for m in 0..12 {
        for d in 0..lengths[m] {
            names.push(format!("{:02}-{:02}", m + 1, d + 1));
        }
    }
    let mut seed = 2409;
    let mut stays: Vec<(usize, usize, usize, usize)> = Vec::new();
    for _ in 0..100000 {
        let (a, b) = (next_random(&mut seed) % 365, next_random(&mut seed) % 365);
        let (c, d) = (next_random(&mut seed) % 365, next_random(&mut seed) % 365);
        stays.push((a.min(b) as usize, a.max(b) as usize, c.min(d) as usize, c.max(d) as usize));
    }
    let mut check: i64 = 0;
    for p in 0..100 {
        for &(a, b, c, d) in &stays {
            check = (check * 31 + count_days_together(&names[a], &names[b], &names[c], &names[d]) + p) % 1000000007;
        }
    }
    println!("100 passes over 10^5 pairs of stays: checksum {}", check);
}
