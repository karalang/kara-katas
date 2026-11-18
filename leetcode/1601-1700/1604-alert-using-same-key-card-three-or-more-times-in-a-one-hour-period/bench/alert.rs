// LeetCode #1604: Alert Using Same Key-Card Three or More Times in a One
// Hour Period -- the bench in Rust, mirroring alert.kara: each name's
// minutes in a `BTreeMap<String, Vec<i32>>`, each list sorted.

use std::collections::BTreeMap;

const NAMES: [&str; 8] = ["daniel", "luis", "alice", "bob", "john", "leslie", "clare", "anna"];

fn minutes(t: &str) -> i32 {
    let (h, m) = t.split_once(':').unwrap();
    h.parse::<i32>().unwrap() * 60 + m.parse::<i32>().unwrap()
}

fn alert_names(key_name: &[String], key_time: &[String]) -> Vec<String> {
    let mut uses: BTreeMap<String, Vec<i32>> = BTreeMap::new();
    for (name, time) in key_name.iter().zip(key_time.iter()) {
        uses.entry(name.clone()).or_insert_with(Vec::new).push(minutes(time));
    }
    let mut out = Vec::new();
    for (name, times) in uses.iter_mut() {
        times.sort();
        if (2..times.len()).any(|i| times[i] - times[i - 2] <= 60) {
            out.push(name.clone());
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1604;
    let mut days = Vec::new();
    for _ in 0..30 {
        let mut names = Vec::new();
        let mut times = Vec::new();
        for _ in 0..100000 {
            let who = big(&mut seed) % 20000;
            names.push(if who < 8 { NAMES[who as usize].to_string() } else { format!("{}{}", NAMES[(who % 8) as usize], who / 8) });
            let t = big(&mut seed) % 1440;
            times.push(format!("{:02}:{:02}", t / 60, t % 60));
        }
        days.push((names, times));
    }
    let mut check = 0;
    let mut alerts = 0;
    for (names, times) in days.iter() {
        for name in alert_names(names, times).iter() {
            alerts += 1;
            for b in name.bytes() {
                check = mix(check, b as i64);
            }
            check = mix(check, 0);
        }
    }
    println!("30 days of 100000 swipes by 20000 names: {} alerts, checksum {}", alerts, check);
}
