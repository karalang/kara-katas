// Benchmark harness for LeetCode #134 — Gas Station.
// Mirrors gas_station.kara algorithm-for-algorithm.

fn can_complete(gas: &[i64], cost: &[i64]) -> i64 {
    let n = gas.len();
    let mut total: i64 = 0;
    let mut tank: i64 = 0;
    let mut start: i64 = 0;
    for i in 0..n {
        let d = gas[i] - cost[i];
        total += d;
        tank += d;
        if tank < 0 {
            start = i as i64 + 1;
            tank = 0;
        }
    }
    if total >= 0 {
        start
    } else {
        -1
    }
}

fn lcg(seed: i64, n: i64, cap: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut x = seed;
    for _ in 0..n {
        x = (x * 1103515245 + 12345) % 2147483648;
        out.push((x / 65536) % cap);
    }
    out
}

fn main() {
    let np: i64 = 8;
    let n: i64 = 200000;
    let iters: i64 = 1200;

    let mut gases: Vec<Vec<i64>> = Vec::new();
    let mut costs: Vec<Vec<i64>> = Vec::new();
    for j in 0..np {
        gases.push(lcg(j + 1, n, 100));
        if j % 2 == 0 {
            costs.push(lcg(j + 100, n, 90));
        } else {
            costs.push(lcg(j + 100, n, 110));
        }
    }

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        sink = (sink + can_complete(&gases[idx], &costs[idx])) % 1000000007;
    }
    println!("{}", sink);
}
