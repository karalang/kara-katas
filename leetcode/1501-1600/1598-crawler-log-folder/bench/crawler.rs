// LeetCode #1598: Crawler Log Folder
// -- the bench in Rust, mirroring crawler.kara: only the depth matters,
// read by matching each log, on 2000 logs of 5000 operations, all drawn
// first.

fn min_operations(logs: &[String]) -> i32 {
    let mut depth: i32 = 0;
    for log in logs {
        match log.as_str() {
            "../" => depth = (depth - 1).max(0),
            "./" => {}
            _ => depth += 1,
        }
    }
    depth
}

fn main() {
    let mut seed: i64 = 1598;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let all: Vec<Vec<String>> = (0..2000)
        .map(|_| {
            (0..5000)
                .map(|_| {
                    let r = next_random() % 8;
                    if r < 2 { "../".to_string() } else if r < 4 { "./".to_string() } else { format!("d{}/", r - 3) }
                })
                .collect()
        })
        .collect();
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for logs in &all {
        let answer = min_operations(logs);
        total += answer as i64;
        check = (check * 31 + answer as i64 + 1) % 1000000007;
    }
    println!("2000 logs of 5000 operations: total {}, checksum {}", total, check);
}
