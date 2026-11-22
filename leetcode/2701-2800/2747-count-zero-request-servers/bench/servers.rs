// LeetCode #2747: Count Zero Request Servers -- the bench (servers.kara in
// Rust): the logs sorted by time, the queries in time order, and a window
// of logs sliding forward with a count for each server.

fn count_servers(n: i64, logs: &[Vec<i64>], x: i64, queries: &[i64]) -> Vec<i64> {
    let mut by_time: Vec<(i64, i64)> = logs.iter().map(|log| (log[1], log[0])).collect();
    by_time.sort();
    let mut order: Vec<usize> = (0..queries.len()).collect();
    order.sort_by_key(|&i| queries[i]);
    let mut requests: Vec<i64> = vec![0; (n + 1) as usize];
    let mut busy = 0;
    let mut answers: Vec<i64> = vec![0; queries.len()];
    let (mut start, mut end) = (0, 0);
    for &i in order.iter() {
        let q = queries[i];
        while end < by_time.len() && by_time[end].0 <= q {
            let server = by_time[end].1 as usize;
            if requests[server] == 0 {
                busy += 1;
            }
            requests[server] += 1;
            end += 1;
        }
        while start < end && by_time[start].0 < q - x {
            let server = by_time[start].1 as usize;
            requests[server] -= 1;
            if requests[server] == 0 {
                busy -= 1;
            }
            start += 1;
        }
        answers[i] = n - busy;
    }
    answers
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10;
    let rounds = 3;
    let n = 100000;
    let mut seed = 2747;
    let mut cases: Vec<(Vec<Vec<i64>>, i64, Vec<i64>)> = Vec::new();
    for _ in 0..count {
        let x = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
        let mut logs: Vec<Vec<i64>> = Vec::new();
        for _ in 0..100000 {
            let server = next_random(&mut seed) % n + 1;
            let hi = next_random(&mut seed);
            let time = (hi * 32768 + next_random(&mut seed)) % 1000000 + 1;
            logs.push(vec![server, time]);
        }
        let queries: Vec<i64> = (0..100000)
            .map(|_| {
                let hi = next_random(&mut seed);
                x + 1 + (hi * 32768 + next_random(&mut seed)) % (1000000 - x)
            })
            .collect();
        cases.push((logs, x, queries));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (logs, x, queries) in cases.iter() {
            for &a in count_servers(n, logs, *x, queries).iter() {
                sum += a;
                check = (check * 31 + a + r) % 1000000007;
            }
        }
    }
    println!("{count} cases of 100000 logs and queries, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
