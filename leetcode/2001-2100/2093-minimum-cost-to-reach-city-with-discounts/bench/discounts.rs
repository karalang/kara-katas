// LeetCode #2093: Minimum Cost to Reach City With Discounts -- Rust mirror
// of the ★ arm's benchmark (discounts.kara): the same 60 maps, each asked
// by the same Dijkstra over (city, used) states with a `BinaryHeap`.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn minimum_cost(n: usize, highways: &[(usize, usize, i64)], discounts: usize) -> i64 {
    let mut roads: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for &(a, b, toll) in highways {
        roads[a].push((b, toll));
        roads[b].push((a, toll));
    }
    let k = discounts + 1;
    let mut best = vec![i64::MAX; n * k];
    let mut heap: BinaryHeap<Reverse<(i64, usize, usize)>> = BinaryHeap::new();
    best[0] = 0;
    heap.push(Reverse((0, 0, 0)));
    while let Some(Reverse((cost, city, used))) = heap.pop() {
        if city == n - 1 {
            return cost;
        }
        if cost > best[city * k + used] {
            continue;
        }
        for &(other, toll) in &roads[city] {
            let full = cost + toll;
            if full < best[other * k + used] {
                best[other * k + used] = full;
                heap.push(Reverse((full, other, used)));
            }
            if used < discounts {
                let half = cost + toll / 2;
                if half < best[other * k + used + 1] {
                    best[other * k + used + 1] = half;
                    heap.push(Reverse((half, other, used + 1)));
                }
            }
        }
    }
    -1
}

fn main() {
    let mut seed = 2093;
    let n = 20000usize;
    let mut total = 0i64;
    let mut check = 0i64;
    for g in 0..60usize {
        let mut highways: Vec<(usize, usize, i64)> = Vec::new();
        for a in 0..n {
            for base in [1usize, 1667, 3333] {
                let b = (a + base + (next_random(&mut seed) % 1666) as usize) % n;
                let hi = next_random(&mut seed);
                let toll = (hi * 32768 + next_random(&mut seed)) % 100001;
                highways.push((a, b, toll));
            }
        }
        let c = minimum_cost(n, &highways, g % 12 * 2);
        total += c;
        check = (check * 31 + c + 2) % 1000000007;
    }
    println!("60 answers: sum {}, checksum {}", total, check);
}
