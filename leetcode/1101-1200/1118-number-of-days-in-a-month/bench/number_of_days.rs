// LeetCode #1118: Number of Days in a Month -- the bench in Rust, the
// ★ arm's `match` over the same 10^6 months and 40 rounds.

fn is_leap(year: i32) -> bool {
    year % 4 == 0 && year % 100 != 0 || year % 400 == 0
}

fn number_of_days(year: i32, month: i32) -> i32 {
    match month {
        2 => if is_leap(year) { 29 } else { 28 },
        4 | 6 | 9 | 11 => 30,
        _ => 31,
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1118;
    let mut years: Vec<i32> = Vec::with_capacity(1000000);
    let mut months: Vec<i32> = Vec::with_capacity(1000000);
    for _ in 0..1000000 {
        years.push((1583 + next_random(&mut seed) % 517) as i32);
        months.push((1 + next_random(&mut seed) % 12) as i32);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    let mut last: i32 = 0;
    for _ in 0..40 {
        for i in 0..years.len() {
            let d = number_of_days(years[i] + (last & 1), months[i]);
            total += d as i64;
            if i % 64 == 0 {
                check = (check * 31 + d as i64) % 1000000007;
            }
            last = d;
        }
    }
    println!("40 rounds over 10^6 months: {} days, checksum {}", total, check);
}
