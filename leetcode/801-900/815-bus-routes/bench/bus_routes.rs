// Benchmark for #815: Bus Routes -- mirror of the ★ arm (breadth-first
// search over buses), with the same workload as bus_routes.kara.
use std::collections::{HashMap, HashSet, VecDeque};

fn num_buses_to_destination(routes: &[Vec<i64>], source: i64, target: i64) -> i64 {
    if source == target {
        return 0;
    }
    let mut buses_at: HashMap<i64, Vec<usize>> = HashMap::new();
    for (bus, route) in routes.iter().enumerate() {
        for &stop in route {
            buses_at.entry(stop).or_default().push(bus);
        }
    }
    let first = match buses_at.get(&source) {
        Some(first) => first,
        None => return -1,
    };
    let mut taken = vec![false; routes.len()];
    let mut queue: VecDeque<(usize, i64)> = VecDeque::new();
    for &bus in first {
        taken[bus] = true;
        queue.push_back((bus, 1));
    }
    let mut seen: HashSet<i64> = HashSet::new();
    while let Some((bus, count)) = queue.pop_front() {
        for &stop in &routes[bus] {
            if stop == target {
                return count;
            }
            if !seen.insert(stop) {
                continue;
            }
            for &next in &buses_at[&stop] {
                if !taken[next] {
                    taken[next] = true;
                    queue.push_back((next, count + 1));
                }
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let rounds: i64 = 4000;
    let mut seed: i64 = 815;
    let mut cities: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let mut routes: Vec<Vec<i64>> = Vec::new();
        for _ in 0..100 {
            let len = (1 + next_random(&mut seed) % 200) as usize;
            let mut on: HashSet<i64> = HashSet::new();
            let mut route: Vec<i64> = Vec::new();
            while route.len() < len {
                let stop = next_random(&mut seed) % 20000;
                if on.insert(stop) {
                    route.push(stop);
                }
            }
            routes.push(route);
        }
        cities.push(routes);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = (round % count as i64) as usize;
        let mut ends: Vec<i64> = Vec::new();
        for _ in 0..2 {
            if next_random(&mut seed) % 8 == 0 {
                ends.push(next_random(&mut seed) % 20000);
            } else {
                let route = &cities[g][(next_random(&mut seed) % 100) as usize];
                ends.push(route[(next_random(&mut seed) % route.len() as i64) as usize]);
            }
        }
        let answer = num_buses_to_destination(&cities[g], ends[0], ends[1]);
        total += answer;
        checksum = (checksum * 31 + answer + 2) % 1000000007;
    }
    println!(
        "{} rounds of 100 routes: total {}, checksum {}",
        rounds, total, checksum
    );
}
