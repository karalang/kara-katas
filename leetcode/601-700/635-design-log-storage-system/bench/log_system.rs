// LeetCode #635: Design Log Storage System -- benchmark, Rust.
//
// The ★ arm: timestamps compared as text after cutting them, and the
// bounds, to the granularity's length.

struct LogSystem {
    logs: Vec<(i64, String)>,
}

impl LogSystem {
    fn new() -> LogSystem {
        LogSystem { logs: Vec::new() }
    }

    fn put(&mut self, id: i64, timestamp: &str) {
        self.logs.push((id, timestamp.to_string()));
    }

    fn retrieve(&self, start: &str, end: &str, granularity: &str) -> Vec<i64> {
        let n = length(granularity);
        let low = &start[..n];
        let high = &end[..n];
        let mut ids = Vec::new();
        for (id, timestamp) in self.logs.iter() {
            let cut = &timestamp[..n];
            if cut >= low && cut <= high {
                ids.push(*id);
            }
        }
        ids
    }
}

fn length(granularity: &str) -> usize {
    match granularity {
        "Year" => 4,
        "Month" => 7,
        "Day" => 10,
        "Hour" => 13,
        "Minute" => 16,
        _ => 19,
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_time(seed: &mut i64) -> String {
    let year = 2000 + next_random(seed) % 18;
    let month = 1 + next_random(seed) % 12;
    let day = 1 + next_random(seed) % 31;
    let hour = next_random(seed) % 24;
    let minute = next_random(seed) % 60;
    let second = next_random(seed) % 60;
    format!("{year}:{month:02}:{day:02}:{hour:02}:{minute:02}:{second:02}")
}

fn main() {
    let names = ["Year", "Month", "Day", "Hour", "Minute", "Second"];
    let mut seed: i64 = 635;
    let mut logs = LogSystem::new();
    for id in 1..20001 {
        let t = random_time(&mut seed);
        logs.put(id, &t);
    }
    let mut found: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..2000 {
        let start = random_time(&mut seed);
        let end = random_time(&mut seed);
        let granularity = names[(next_random(&mut seed) % 6) as usize];
        let ids = logs.retrieve(&start, &end, granularity);
        for id in ids.iter() {
            found += 1;
            checksum = (checksum * 31 + *id) % 1000000007;
        }
    }
    println!("20000 logs, 2000 retrieves: {found} ids, checksum {checksum}");
}
