// LeetCode #2492: Minimum Score of a Path Between Two Cities -- Rust mirror
// of the benchmark (score.kara): the same map, passes and checksum, the
// breadth-first search over a Vec of adjacency Vecs built on every ask.

fn min_score(n: i64, roads: &[[i64; 3]]) -> i64 {
    let n = n as usize;
    let mut next: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n + 1];
    for r in roads {
        next[r[0] as usize].push((r[1] as usize, r[2]));
        next[r[1] as usize].push((r[0] as usize, r[2]));
    }
    let mut seen = vec![false; n + 1];
    let mut queue: Vec<usize> = vec![1];
    seen[1] = true;
    let mut head = 0;
    let mut least = i64::MAX;
    while head < queue.len() {
        let city = queue[head];
        head += 1;
        for &(other, distance) in &next[city] {
            least = least.min(distance);
            if !seen[other] {
                seen[other] = true;
                queue.push(other);
            }
        }
    }
    least
}

fn main() {
    let n: i64 = 100000;
    let passes: i64 = 50;
    let mut seed: i64 = 2492;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut roads: Vec<[i64; 3]> = vec![[1, n, 10000]];
    while (roads.len() as i64) < n {
        let a = (next_random() * 32768 + next_random()) % n + 1;
        let b = (next_random() * 32768 + next_random()) % n + 1;
        if a != b {
            roads.push([a, b, next_random() % 10000 + 1]);
        }
    }
    let m = roads.len() as i64;
    let mut check: i64 = 0;
    for p in 0..passes {
        let at = (check % m) as usize;
        let was = roads[at][2];
        roads[at][2] = (check / m + p) % 10000 + 1;
        check = (check * 31 + min_score(n, &roads) + p) % 1000000007;
        roads[at][2] = was;
    }
    println!("{passes} passes over 10^5 cities and {m} roads: checksum {check}");
}
