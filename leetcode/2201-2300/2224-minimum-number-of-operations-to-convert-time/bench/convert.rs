// LeetCode #2224: Minimum Number of Operations to Convert Time -- the
// benchmark's Rust mirror of convert.kara: each time read from its four
// digits, the gap in minutes cut greedily by 60s, 15s, 5s and 1s.

fn minutes_of(time: &str) -> i64 {
    let d: Vec<i64> = time.chars().filter(|&c| c != ':').map(|c| c as i64 - '0' as i64).collect();
    (d[0] * 10 + d[1]) * 60 + d[2] * 10 + d[3]
}

fn convert_time(current: &str, correct: &str) -> i64 {
    let mut gap = minutes_of(correct) - minutes_of(current);
    let mut operations = 0i64;
    for step in [60i64, 15, 5, 1] {
        operations += gap / step;
        gap %= step;
    }
    operations
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // every time of the day as "HH:MM", built once
    let times: Vec<String> = (0..1440).map(|m| format!("{:02}:{:02}", m / 60, m % 60)).collect();
    let mut seed = 2224i64;
    let mut check = 0i64;
    for _ in 0..2000000 {
        let a = next_random(&mut seed) % 1440;
        let b = next_random(&mut seed) % 1440;
        let (low, high) = if a <= b { (a, b) } else { (b, a) };
        check = (check * 31 + convert_time(&times[low as usize], &times[high as usize])) % 1000000007;
    }
    println!("2000000 pairs: checksum {}", check);
}
