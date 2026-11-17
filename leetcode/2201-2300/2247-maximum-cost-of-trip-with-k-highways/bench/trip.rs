// LeetCode #2247: Maximum Cost of Trip With K Highways -- the benchmark's
// Rust mirror of trip.kara: dynamic programming over subsets, masks in
// increasing order.

fn maximum_cost(n: usize, highways: &[[i64; 3]], k: usize) -> i64 {
    if k + 1 > n {
        return -1;
    }
    let mut roads: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for h in highways {
        roads[h[0] as usize].push((h[1] as usize, h[2]));
        roads[h[1] as usize].push((h[0] as usize, h[2]));
    }
    let full = 1usize << n;
    let mut best = vec![vec![-1i64; n]; full];
    for v in 0..n {
        best[1 << v][v] = 0;
    }
    let mut answer = -1;
    for mask in 1..full {
        let cities = mask.count_ones() as usize;
        for v in 0..n {
            let cost = best[mask][v];
            if cost < 0 {
                continue;
            }
            if cities == k + 1 {
                answer = answer.max(cost);
                continue;
            }
            for &(w, toll) in &roads[v] {
                if mask & (1 << w) == 0 {
                    let next = mask | (1 << w);
                    best[next][w] = best[next][w].max(cost + toll);
                }
            }
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2247i64;
    let mut check = 0i64;
    for _ in 0..16 {
        let mut pairs: Vec<(i64, i64)> = Vec::new();
        for a in 0..15 {
            for b in a + 1..15 {
                pairs.push((a, b));
            }
        }
        for i in (1..pairs.len()).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            pairs.swap(i, j);
        }
        let highways: Vec<[i64; 3]> = pairs.iter().take(50).map(|&(a, b)| [a, b, next_random(&mut seed) % 101]).collect();
        check = (check * 31 + maximum_cost(15, &highways, 14) + 1) % 1000000007;
    }
    println!("16 maps of 15 cities: checksum {}", check);
}
