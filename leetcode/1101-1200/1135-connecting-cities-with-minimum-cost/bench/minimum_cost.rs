// LeetCode #1135: Connecting Cities With Minimum Cost -- the bench in Rust,
// the same algorithm and workload as minimum_cost.kara: each road its own
// `Vec<i64>`, the roads cloned and sorted with `sort_by_key` in every call,
// the same 8 networks and 50 rounds.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut x = x;
    while parent[x as usize] != x {
        parent[x as usize] = parent[parent[x as usize] as usize];
        x = parent[x as usize];
    }
    x
}

fn minimum_cost(n: i64, connections: &[Vec<i64>]) -> i64 {
    let mut roads = connections.to_vec();
    roads.sort_by_key(|road| road[2]);
    let mut parent: Vec<i64> = (0..n + 1).collect();
    let mut size = vec![1i64; (n + 1) as usize];
    let mut total = 0;
    let mut joined = 1;
    for road in roads.iter() {
        let mut a = find(&mut parent, road[0]);
        let mut b = find(&mut parent, road[1]);
        if a != b {
            if size[a as usize] < size[b as usize] {
                std::mem::swap(&mut a, &mut b);
            }
            parent[b as usize] = a;
            size[a as usize] += size[b as usize];
            total += road[2];
            joined += 1;
        }
    }
    if joined == n { total } else { -1 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1135;
    let mut networks: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..8 {
        let mut roads: Vec<Vec<i64>> = Vec::new();
        for _ in 0..10000 {
            let x = next_random(&mut seed) % 1000 + 1;
            let mut y = next_random(&mut seed) % 999 + 1;
            if y >= x {
                y += 1;
            }
            let high = next_random(&mut seed);
            roads.push(vec![x, y, (high * 32768 + next_random(&mut seed)) % 100000 + 1]);
        }
        networks.push(roads);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..50i64 {
        for j in 0..8usize {
            let at = ((round * 7919 + j as i64 * 104729) % 10000) as usize;
            networks[j][at][2] = (networks[j][at][2] * 7 + 13) % 100000 + 1;
            let r = minimum_cost(1000, &networks[j]);
            total += r;
            check = (check * 31 + r + 1) % 1000000007;
        }
    }
    println!("50 rounds over 8 networks of 1000 cities and 10000 roads: costs total {}, checksum {}", total, check);
}
