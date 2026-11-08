// LeetCode #1507: Reformat Date -- the bench: 100000 dates built once,
// then each reformatted ten times by the ★ arm.

const MONTHS: [&str; 12] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

fn reformat_date(date: &str) -> String {
    let parts: Vec<String> = date.split(' ').map(|p| p.to_string()).collect();
    let digits: String = parts[0].chars().take_while(|c| c.is_ascii_digit()).collect();
    let day: i64 = digits.parse().unwrap();
    let month = MONTHS.iter().position(|m| *m == parts[1]).unwrap() + 1;
    format!("{}-{:02}-{:02}", parts[2], month, day)
}

fn suffix(day: i64) -> &'static str {
    match day {
        1 | 21 | 31 => "st",
        2 | 22 => "nd",
        3 | 23 => "rd",
        _ => "th",
    }
}

fn days_in(month: i64, year: i64) -> i64 {
    let days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    let leap = year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
    if month == 1 && leap { 29 } else { days[month as usize] }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1507;
    let mut dates: Vec<String> = Vec::new();
    for _ in 0..100000 {
        let year = 1900 + next_random(&mut seed) % 201;
        let month = next_random(&mut seed) % 12;
        let day = 1 + next_random(&mut seed) % days_in(month, year);
        dates.push(format!("{}{} {} {}", day, suffix(day), MONTHS[month as usize], year));
    }
    let mut check: i64 = 0;
    for _ in 0..10 {
        for date in &dates {
            let out = reformat_date(date);
            for b in out.bytes() {
                check = (check * 31 + b as i64 + 1) % 1000000007;
            }
        }
    }
    println!("1000000 dates reformatted, 100000 built once: checksum {}", check);
}
