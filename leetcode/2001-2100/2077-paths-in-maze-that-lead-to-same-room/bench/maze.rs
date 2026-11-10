// LeetCode #2077: Paths in Maze That Lead to Same Room -- Rust mirror of
// the ★ arm's benchmark (maze.kara): 30 mazes of 1000 rooms and about
// 38000 corridors; each room's rooms above it a `HashSet`, and every
// corridor's triangles its two rooms' sets' `intersection(..).count()`.
use std::collections::HashSet;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_maze(n: i64, count: i64, near: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let mut seen: HashSet<i64> = HashSet::new();
    let mut corridors = Vec::new();
    for _ in 0..count {
        let a = next_random(seed) % n + 1;
        let step = next_random(seed) % near.min(n - 1) + 1;
        let b = (a - 1 + step) % n + 1;
        let key = a.min(b) * 100000 + a.max(b);
        if !seen.contains(&key) {
            seen.insert(key);
            corridors.push(if next_random(seed) % 2 == 0 { vec![a, b] } else { vec![b, a] });
        }
    }
    corridors
}

fn number_of_paths(n: i64, corridors: &[Vec<i64>]) -> i64 {
    let mut up: Vec<HashSet<i64>> = (0..=n).map(|_| HashSet::new()).collect();
    for c in corridors {
        let (a, b) = (c[0].min(c[1]), c[0].max(c[1]));
        up[a as usize].insert(b);
    }
    let mut count = 0;
    for a in 1..=n as usize {
        for b in up[a].iter() {
            count += up[a].intersection(&up[*b as usize]).count() as i64;
        }
    }
    count
}

fn main() {
    let mut seed = 2077;
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..30 {
        let corridors = random_maze(1000, 60000, 60, &mut seed);
        let a = number_of_paths(1000, &corridors);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("30 mazes: sum {}, checksum {}", total, check);
}
