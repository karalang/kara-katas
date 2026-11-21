// LeetCode #2432: The Employee That Worked on the Longest Task -- the
// bench, the ★ arm: one pass with the last leave time in hand, the best
// replaced by a longer task or an equal one of a smaller id.

fn hardest_worker(n: i64, logs: &[Vec<i64>]) -> i64 {
    let mut best_id = n;
    let mut best_time = 0;
    let mut start = 0;
    for log in logs.iter() {
        let time = log[1] - start;
        if time > best_time || (time == best_time && log[0] < best_id) {
            best_time = time;
            best_id = log[0];
        }
        start = log[1];
    }
    best_id
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2432;
    let mut cases: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..2000 {
        let mut logs: Vec<Vec<i64>> = Vec::new();
        let mut time = 0;
        let mut last = -1;
        for _ in 0..500 {
            let mut id = next_random(&mut seed) % 500;
            if id == last {
                id = (id + 1) % 500;
            }
            time += 1 + next_random(&mut seed) % 3;
            logs.push(vec![id, time]);
            last = id;
        }
        cases.push(logs);
    }
    let mut check: i64 = 0;
    for p in 0..50i64 {
        for c in 0..cases.len() {
            cases[c][499][1] += 1;
            check = (check * 31 + hardest_worker(500, &cases[c]) + p) % 1000000007;
        }
    }
    println!("50 passes over 2000 cases of 500 logs: checksum {}", check);
}
