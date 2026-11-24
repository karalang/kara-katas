// LeetCode #1344 bench in Rust: the ★ arm (the hour hand 30 degrees an
// hour plus half a degree a minute, the minute hand 6 a minute, and the
// smaller of the gap and 360 less it) on the same 3 * 10^7 times.

fn angle_clock(hour: i32, minutes: i32) -> f64 {
    let hour_hand = (hour % 12) as f64 * 30.0 + minutes as f64 * 0.5;
    let minute_hand = minutes as f64 * 6.0;
    let gap = (hour_hand - minute_hand).abs();
    gap.min(360.0 - gap)
}

fn main() {
    let mut check: i64 = 0;
    for i in 0..30000000i64 {
        let since = (i + check) % 720;
        let mut hour = since / 60;
        if hour == 0 {
            hour = 12;
        }
        let a = angle_clock(hour as i32, (since % 60) as i32);
        check = (check * 31 + (2.0 * a) as i64) % 1000000007;
    }
    println!("3 * 10^7 times: checksum {}", check);
}
