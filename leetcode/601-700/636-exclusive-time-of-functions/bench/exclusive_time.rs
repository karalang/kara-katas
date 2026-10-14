// LeetCode #636: Exclusive Time of Functions -- benchmark, Rust.
//
// The ★ arm: one stack of running functions and the time of the last
// event.

fn exclusive_time(n: usize, logs: &[String]) -> Vec<i64> {
    let mut total = vec![0i64; n];
    let mut stack: Vec<usize> = Vec::new();
    let mut prev = 0i64;
    for log in logs {
        let parts: Vec<&str> = log.split(':').collect();
        let id: usize = parts[0].parse().unwrap();
        let t: i64 = parts[2].parse().unwrap();
        if parts[1] == "start" {
            if let Some(&top) = stack.last() {
                total[top] += t - prev;
            }
            stack.push(id);
            prev = t;
        } else {
            let top = stack.pop().unwrap();
            total[top] += t - prev + 1;
            prev = t + 1;
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn random_logs(n: i64, calls: i64, gap: i64, seed: &mut i64) -> Vec<String> {
    let mut logs = Vec::new();
    let mut stack = Vec::new();
    let mut started = 0;
    let mut start_at = 0;
    let mut end_at = 0;
    while started < calls || !stack.is_empty() {
        let begin = started < calls && (stack.is_empty() || next_random(seed) % 2 == 0);
        if begin {
            let id = next_random(seed) % n;
            let t = start_at + wide(seed) % gap;
            logs.push(format!("{id}:start:{t}"));
            stack.push(id);
            started += 1;
            start_at = t + 1;
            end_at = t;
        } else {
            let id = stack.pop().unwrap();
            let t = end_at + wide(seed) % gap;
            logs.push(format!("{id}:end:{t}"));
            start_at = t + 1;
            end_at = t + 1;
        }
    }
    logs
}

fn main() {
    let mut seed: i64 = 636;
    let inputs: Vec<Vec<String>> = (0..10).map(|_| random_logs(100, 250, 3800000, &mut seed)).collect();
    let mut sum: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..10000 {
        for t in exclusive_time(100, &inputs[round % 10]) {
            sum += t;
            checksum = (checksum * 31 + t) % 1000000007;
        }
    }
    println!("10 inputs of 500 logs, 10000 rounds: total {sum}, checksum {checksum}");
}
