// LeetCode #1360 bench -- Rust: each date as its count of days from
// 1971-01-01, the answer the two counts' distance.
const LENGTHS: [i64; 12] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

fn is_leap(year: i64) -> bool {
    (year % 4 == 0 && year % 100 != 0) || year % 400 == 0
}

fn days_from_1971(date: &str) -> i64 {
    let year: i64 = date[0..4].parse().unwrap();
    let month: i64 = date[5..7].parse().unwrap();
    let day: i64 = date[8..10].parse().unwrap();
    let mut days = day - 1;
    for y in 1971..year {
        days += if is_leap(y) { 366 } else { 365 };
    }
    for m in 1..month {
        days += LENGTHS[(m - 1) as usize];
        if m == 2 && is_leap(year) {
            days += 1;
        }
    }
    days
}

fn days_between_dates(date1: &str, date2: &str) -> i32 {
    (days_from_1971(date1) - days_from_1971(date2)).abs() as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_date(seed: &mut i64) -> String {
    let year = 1971 + next_random(seed) % 130;
    let month = 1 + next_random(seed) % 12;
    let mut last = LENGTHS[(month - 1) as usize];
    if month == 2 && is_leap(year) {
        last += 1;
    }
    let day = 1 + next_random(seed) % last;
    format!("{}-{:02}-{:02}", year, month, day)
}

fn main() {
    // 1000 dates written once; then 3 * 10^5 questions, each pair of dates
    // drawn from the checksum so far, every answer folded into it
    let mut seed = 1360;
    let dates: Vec<String> = (0..1000).map(|_| random_date(&mut seed)).collect();
    let mut check: i64 = 0;
    for r in 0..300000 {
        let a = (check % 1000) as usize;
        let b = ((check / 1000 + r) % 1000) as usize;
        check = (check * 31 + days_between_dates(&dates[a], &dates[b]) as i64 + r) % 1000000007;
    }
    println!("300000 questions: checksum {}", check);
}
