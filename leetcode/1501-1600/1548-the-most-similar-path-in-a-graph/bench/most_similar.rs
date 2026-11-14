// LeetCode #1548: The Most Similar Path in a Graph -- bench: the ★ arm (a
// DP over the target's places) over 100 connected graphs of 50 to 100
// cities named from up to 26 names, each with a target of 100 names, built
// once, each asked 20 times. Rust mirror of most_similar.kara.

fn most_similar(n: i64, roads: &[(i64, i64)], names: &[String], target: &[String]) -> Vec<i64> {
    let n = n as usize;
    let mut next_to: Vec<Vec<i64>> = vec![Vec::new(); n];
    for &(a, b) in roads {
        next_to[a as usize].push(b);
        next_to[b as usize].push(a);
    }
    let length = target.len();
    let mut cost = vec![vec![i64::MAX; n]; length];
    let mut from = vec![vec![0i64; n]; length];
    for v in 0..n {
        cost[0][v] = if names[v] == target[0] { 0 } else { 1 };
    }
    for t in 1..length {
        for v in 0..n {
            let miss = if names[v] == target[t] { 0 } else { 1 };
            for &u in &next_to[v] {
                let u = u as usize;
                if cost[t - 1][u] + miss < cost[t][v] {
                    cost[t][v] = cost[t - 1][u] + miss;
                    from[t][v] = u as i64;
                }
            }
        }
    }
    let mut last = 0;
    for v in 1..n {
        if cost[length - 1][v] < cost[length - 1][last] {
            last = v;
        }
    }
    let mut path = vec![0i64; length];
    path[length - 1] = last as i64;
    for t in (1..length).rev() {
        path[t - 1] = from[t][path[t] as usize];
    }
    path
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn name_of(i: i64) -> String {
    let letters = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let mut name = String::new();
    for place in [676, 26, 1] {
        name.push(letters[(i / place % 26) as usize] as char);
    }
    name
}

fn main() {
    let mut seed = 1548i64;
    let mut graphs = Vec::new();
    for _ in 0..100 {
        let n = next_random(&mut seed) % 51 + 50;
        let own = next_random(&mut seed) % 26 + 1;
        let names: Vec<String> = (0..n).map(|_| name_of(next_random(&mut seed) % own)).collect();
        let nu = n as usize;
        let mut joined = vec![vec![false; nu]; nu];
        let mut roads = Vec::new();
        for v in 1..n {
            let u = next_random(&mut seed) % v;
            joined[u as usize][v as usize] = true;
            joined[v as usize][u as usize] = true;
            roads.push((v, u));
        }
        let extra = next_random(&mut seed) % (4 * n);
        for _ in 0..extra {
            let a = next_random(&mut seed) % n;
            let b = next_random(&mut seed) % n;
            if a != b && !joined[a as usize][b as usize] {
                joined[a as usize][b as usize] = true;
                joined[b as usize][a as usize] = true;
                roads.push((a, b));
            }
        }
        let target: Vec<String> = (0..100).map(|_| name_of(next_random(&mut seed) % (own + 1))).collect();
        graphs.push((n, roads, names, target));
    }
    let mut check = 0i64;
    let mut total = 0i64;
    for _ in 0..20 {
        for (n, roads, names, target) in &graphs {
            let path = most_similar(*n, roads, names, target);
            let mut distance = 0;
            for t in 0..path.len() {
                check = mix(check, path[t]);
                if names[path[t] as usize] != target[t] {
                    distance += 1;
                }
            }
            total += distance;
        }
    }
    println!("20 passes over 100 graphs of up to 100 cities: distance {}, checksum {}", total, check);
}
