// LeetCode #1154 bench -- mirrors day_of_year.kara: the same dates, the
// same passes, the ★ arm's table.

const BEFORE: [i64; 12] = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];

fn is_leap(year: i64) -> bool {
    year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)
}

fn day_of_year(date: &str) -> i64 {
    let year: i64 = date[0..4].parse().unwrap();
    let month: i64 = date[5..7].parse().unwrap();
    let day: i64 = date[8..10].parse().unwrap();
    let leap_day = if month > 2 && is_leap(year) { 1 } else { 0 };
    BEFORE[(month - 1) as usize] + day + leap_day
}

fn days_in(year: i64, month: i64) -> i64 {
    if month == 2 {
        if year % 400 == 0 || (year % 4 == 0 && year % 100 != 0) { 29 } else { 28 }
    } else {
        31 - (month - 1) % 7 % 2
    }
}

fn main() {
    let passes = 1000;
    let mut dates: Vec<String> = Vec::new();
    for year in 1900..2020 {
        for month in 1..13 {
            for day in 1..days_in(year, month) + 1 {
                dates.push(format!("{year}-{month:02}-{day:02}"));
            }
        }
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for p in 0..passes {
        for date in dates.iter() {
            let n = day_of_year(date);
            total += n;
            check = (check * 31 + n + p) % 1000000007;
        }
    }
    println!("{passes} passes over {} dates: total {total}, checksum {check}", dates.len());
}
