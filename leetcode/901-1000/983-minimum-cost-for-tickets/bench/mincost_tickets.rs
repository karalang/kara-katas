// Benchmark: LeetCode #983 Minimum Cost For Tickets -- the ★ arm, a
// table over the calendar, on plans of up to LeetCode's 365 days.
// Mirrors mincost_tickets.kara, .c, .py and go-seq/.

fn mincost_tickets(days: &[i64], costs: &[i64]) -> i64 {
    let last = days[days.len() - 1] as usize;
    let mut travel = vec![false; last + 1];
    for &d in days {
        travel[d as usize] = true;
    }
    let mut best = vec![0i64; last + 1];
    for d in 1..last + 1 {
        if !travel[d] {
            best[d] = best[d - 1];
            continue;
        }
        let week = if d >= 7 { best[d - 7] } else { 0 };
        let month = if d >= 30 { best[d - 30] } else { 0 };
        best[d] = (best[d - 1] + costs[0]).min(week + costs[1]).min(month + costs[2]);
    }
    best[last]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 300;
    let mut seed = 983;
    let mut plans: Vec<Vec<i64>> = Vec::new();
    let mut prices: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let n = 1 + next_random(&mut seed) % 365;
        let mut days = Vec::new();
        let mut need = n;
        for d in 1..366i64 {
            if need > 0 && next_random(&mut seed) % (366 - d) < need {
                days.push(d);
                need -= 1;
            }
        }
        plans.push(days);
        let a = 1 + next_random(&mut seed) % 1000;
        let b = 1 + next_random(&mut seed) % 1000;
        let c = 1 + next_random(&mut seed) % 1000;
        prices.push(vec![a, b, c]);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..1000 {
            let j = (r + i) % 1000;
            let c = mincost_tickets(&plans[j], &prices[j]);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    println!("{} rounds over 1000 plans of up to 365 days: cost {}, checksum {}", rounds, total, check);
}
