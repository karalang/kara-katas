// Benchmark for #656: cheapest cost to the end, worked backwards, as the
// Kara ★ arm.

const UNREACHABLE: i64 = i64::MAX;

fn cheapest_jump(coins: &[i64], max_jump: i64) -> Vec<i64> {
    let n = coins.len() as i64;
    let mut cost = vec![UNREACHABLE; n as usize];
    let mut next = vec![-1i64; n as usize];
    if coins[(n - 1) as usize] != -1 {
        cost[(n - 1) as usize] = coins[(n - 1) as usize];
    }
    let mut i = n - 2;
    while i >= 0 {
        let iu = i as usize;
        if coins[iu] != -1 {
            let last = (i + max_jump).min(n - 1);
            for j in (i + 1) as usize..=last as usize {
                if cost[j] != UNREACHABLE && coins[iu] + cost[j] < cost[iu] {
                    cost[iu] = coins[iu] + cost[j];
                    next[iu] = j as i64;
                }
            }
        }
        i -= 1;
    }
    let mut path = Vec::new();
    if cost[0] == UNREACHABLE {
        return path;
    }
    let mut at = 0i64;
    while at != -1 {
        path.push(at + 1);
        at = next[at as usize];
    }
    path
}

fn main() {
    let inputs = 8usize;
    let rounds = 40usize;
    let n = 100000usize;
    let mut seed: i64 = 656;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut rows: Vec<Vec<i64>> = Vec::new();
    for _ in 0..inputs {
        let mut coins = Vec::with_capacity(n);
        for i in 0..n {
            if i > 0 && next_random() % 10 == 0 {
                coins.push(-1);
            } else {
                coins.push(next_random() % 101);
            }
        }
        rows.push(coins);
    }
    let mut steps = 0usize;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let coins = &rows[(r * 3) % inputs];
        let path = cheapest_jump(coins, 100);
        let mut cost = 0i64;
        for &p in &path {
            cost += coins[(p - 1) as usize];
            checksum = (checksum * 31 + p) % 1000000007;
        }
        steps += path.len();
        checksum = (checksum * 31 + cost) % 1000000007;
    }
    println!("{} rows of {}, {} rounds: {} steps, checksum {}", inputs, n, rounds, steps, checksum);
}
