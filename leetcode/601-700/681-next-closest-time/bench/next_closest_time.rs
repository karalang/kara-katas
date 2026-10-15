// LeetCode #681: Next Closest Time -- step a minute at a time. Bench.

fn digits_of(minutes: i64) -> [i64; 4] {
    let h = minutes / 60;
    let m = minutes % 60;
    [h / 10, h % 10, m / 10, m % 10]
}

fn next_closest_time(time: &str) -> String {
    let b = time.as_bytes();
    let h = (b[0] - b'0') as i64 * 10 + (b[1] - b'0') as i64;
    let m = (b[3] - b'0') as i64 * 10 + (b[4] - b'0') as i64;
    let mut allowed = [false; 10];
    for d in digits_of(h * 60 + m) {
        allowed[d as usize] = true;
    }
    let mut now = h * 60 + m;
    loop {
        now = (now + 1) % 1440;
        let mut ok = true;
        for d in digits_of(now) {
            if !allowed[d as usize] {
                ok = false;
            }
        }
        if ok {
            return format!("{}{}:{}{}", now / 600, now / 60 % 10, now % 60 / 10, now % 10);
        }
    }
}

fn main() {
    let rounds: i64 = 300;
    let mut times: Vec<String> = Vec::new();
    for t in 0..1440 {
        times.push(format!("{:02}:{:02}", t / 60, t % 60));
    }
    let mut sum: i64 = 0;
    let mut wrapped: i64 = 0;
    for r in 0..rounds {
        for k in 0..1440i64 {
            let at = (k * 7 + r) % 1440;
            let answer = next_closest_time(&times[at as usize]);
            let b = answer.as_bytes();
            let hour = (b[0] - b'0') as i64 * 10 + (b[1] - b'0') as i64;
            let then = hour * 60 + (b[3] - b'0') as i64 * 10 + (b[4] - b'0') as i64;
            if then <= at {
                wrapped += 1;
            }
            sum = (sum * 1441 + then + 1) % 1000000007;
        }
    }
    println!("{} times: {} answers on the next day, checksum {}", 1440 * rounds, wrapped, sum);
}
