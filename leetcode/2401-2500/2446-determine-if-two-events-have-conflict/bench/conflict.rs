// LeetCode #2446: Determine if Two Events Have Conflict -- the bench, the
// ★ arm: the four `HH:MM` strings compared as text.

fn have_conflict(event1: &[String], event2: &[String]) -> bool {
    event1[0] <= event2[1] && event2[0] <= event1[1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn clock(minute: i64) -> String {
    format!("{:02}:{:02}", minute / 60, minute % 60)
}

fn main() {
    let mut seed = 2446;
    let n: usize = 100000;
    let mut events: Vec<Vec<String>> = Vec::new();
    for _ in 0..n {
        let a = next_random(&mut seed) % 1440;
        let b = next_random(&mut seed) % 1440;
        events.push(vec![clock(a.min(b)), clock(a.max(b))]);
    }
    let mut check: i64 = 0;
    for p in 0..300usize {
        for i in 0..n {
            let j = (7 * i + p + 1) % n;
            let answer = if have_conflict(&events[i], &events[j]) { 1 } else { 0 };
            check = (check * 31 + answer + p as i64) % 1000000007;
        }
    }
    println!("300 passes over 10^5 events: checksum {}", check);
}
