// LeetCode #2477: Minimum Fuel Cost to Report to the Capital -- the bench,
// the ★ arm in Rust: a breadth-first order from the capital, walked
// backwards, gives each city its subtree's size, and the road out of it
// carries `ceil(size / seats)` cars.

fn minimum_fuel_cost(roads: &[Vec<i64>], seats: i64) -> i64 {
    let n = roads.len() + 1;
    let mut adjacent: Vec<Vec<usize>> = vec![Vec::new(); n];
    for road in roads {
        let (a, b) = (road[0] as usize, road[1] as usize);
        adjacent[a].push(b);
        adjacent[b].push(a);
    }
    let mut parent = vec![usize::MAX; n];
    let mut order = vec![0usize];
    parent[0] = 0;
    let mut next = 0;
    while next < order.len() {
        let city = order[next];
        next += 1;
        for &other in &adjacent[city] {
            if parent[other] == usize::MAX {
                parent[other] = city;
                order.push(other);
            }
        }
    }
    let mut size = vec![1i64; n];
    let mut fuel = 0;
    for k in (1..n).rev() {
        let city = order[k];
        fuel += (size[city] + seats - 1) / seats;
        size[parent[city]] += size[city];
    }
    fuel
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn random_roads(n: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let mut roads = Vec::new();
    for k in 1..n {
        let other = wide_random(seed) % k;
        if next_random(seed) % 2 == 0 {
            roads.push(vec![k, other]);
        } else {
            roads.push(vec![other, k]);
        }
    }
    for i in (1..roads.len()).rev() {
        let j = (wide_random(seed) % (i as i64 + 1)) as usize;
        roads.swap(i, j);
    }
    roads
}

fn main() {
    // 20 random trees of 10^4 cities built once; then 60 passes, each
    // answering every tree with 1 to 50 seats chosen by the checksum so
    // far, folding the fuel plus the pass into the checksum
    let mut seed = 2477;
    let trees: Vec<Vec<Vec<i64>>> = (0..20).map(|_| random_roads(10000, &mut seed)).collect();
    let mut check = 0i64;
    for p in 0..60i64 {
        for roads in trees.iter() {
            let seats = 1 + check % 50;
            check = (check * 31 + minimum_fuel_cost(roads, seats) + p) % 1000000007;
        }
    }
    println!("60 passes over 20 trees of 10^4: checksum {check}");
}
