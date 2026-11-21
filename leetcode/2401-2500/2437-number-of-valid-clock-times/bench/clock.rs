// LeetCode #2437: Number of Valid Clock Times -- the bench, the ★ arm:
// the hours that fit the first two characters times the minutes that
// fit the last two.

fn fits(pattern: &[u8], value: i64) -> bool {
    let tens = b'0' + (value / 10) as u8;
    let units = b'0' + (value % 10) as u8;
    (pattern[0] == b'?' || pattern[0] == tens) && (pattern[1] == b'?' || pattern[1] == units)
}

fn count_time(time: &str) -> i64 {
    let b = time.as_bytes();
    let mut hours = 0;
    for h in 0..24 {
        if fits(&b[0..2], h) {
            hours += 1;
        }
    }
    let mut minutes = 0;
    for m in 0..60 {
        if fits(&b[3..5], m) {
            minutes += 1;
        }
    }
    hours * minutes
}

fn main() {
    let mut times: Vec<String> = Vec::new();
    for at in 0..1440 {
        for mask in 0..16 {
            let shown = format!("{:02}:{:02}", at / 60, at % 60);
            let mut out: Vec<u8> = Vec::new();
            let mut digit = 0;
            for &c in shown.as_bytes() {
                if c == b':' {
                    out.push(c);
                } else {
                    out.push(if (mask >> digit) & 1 == 1 { b'?' } else { c });
                    digit += 1;
                }
            }
            times.push(String::from_utf8(out).unwrap());
        }
    }
    let mut check: i64 = 0;
    let n = times.len();
    for p in 0..120usize {
        for i in 0..n {
            check = (check * 31 + count_time(&times[(i * 7 + p) % n]) + p as i64) % 1000000007;
        }
    }
    println!("120 passes over 23040 patterns: checksum {}", check);
}
