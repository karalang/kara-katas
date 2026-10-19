// LeetCode 787 — Cheapest Flights Within K Stops: the bench, in Rust.
// Mirrors find_cheapest_price.kara: Bellman-Ford for k + 1 rounds, each
// round reading a fresh copy of the costs, over the same 64 networks.

fn find_cheapest_price(n: usize, flights: &[[i64; 3]], src: usize, dst: usize, k: i64) -> i64 {
    let unreached = i64::MAX;
    let mut cost = vec![unreached; n];
    cost[src] = 0;
    for _ in 0..k + 1 {
        let before = cost.clone();
        for f in flights {
            let (from, to, price) = (f[0] as usize, f[1] as usize, f[2]);
            if before[from] != unreached && before[from] + price < cost[to] {
                cost[to] = before[from] + price;
            }
        }
    }
    if cost[dst] == unreached { -1 } else { cost[dst] }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 787;
    let mut networks: Vec<Vec<[i64; 3]>> = Vec::new();
    for _ in 0..64 {
        let mut taken = vec![false; 10000];
        let mut flights: Vec<[i64; 3]> = Vec::new();
        while flights.len() < 1000 {
            let from = next_random(&mut seed) % 100;
            let to = next_random(&mut seed) % 100;
            if from != to && !taken[(from * 100 + to) as usize] {
                taken[(from * 100 + to) as usize] = true;
                flights.push([from, to, 1 + next_random(&mut seed) % 10000]);
            }
        }
        networks.push(flights);
    }
    let rounds = 20000;
    let mut found = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let src = next_random(&mut seed) % 100;
        let dst = (src + 1 + next_random(&mut seed) % 99) % 100;
        let k = next_random(&mut seed) % 100;
        let answer = find_cheapest_price(100, &networks[r % 64], src as usize, dst as usize, k);
        if answer != -1 {
            found += 1;
        }
        check = (check * 31 + answer + 1) % 1000000007;
    }
    println!("{rounds} rounds of 100-city networks: {found} with a way, checksum {check}");
}
