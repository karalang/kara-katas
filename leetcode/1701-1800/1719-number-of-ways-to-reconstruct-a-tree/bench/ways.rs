// LeetCode #1719: Number Of Ways To Reconstruct A Tree -- the bench
// (ways.kara): the nodes by degree, most first, each hung under the last
// earlier neighbour, which must hold every other neighbour of it.

fn check_ways(pairs: &[Vec<i32>]) -> i32 {
    let size = 501;
    let mut linked = vec![vec![false; size]; size];
    let mut degree = vec![0i64; size];
    for pair in pairs {
        let (x, y) = (pair[0] as usize, pair[1] as usize);
        linked[x][y] = true;
        linked[y][x] = true;
        degree[x] += 1;
        degree[y] += 1;
    }
    let mut nodes: Vec<usize> = (0..size).filter(|&v| degree[v] > 0).collect();
    let n = nodes.len() as i64;
    nodes.sort_by_key(|&v| -degree[v]);
    if degree[nodes[0]] != n - 1 {
        return 0;
    }
    let mut ways = 1;
    for i in 1..nodes.len() {
        let v = nodes[i];
        let mut parent: i64 = -1;
        for j in (0..i).rev() {
            if linked[v][nodes[j]] {
                parent = nodes[j] as i64;
                break;
            }
        }
        if parent < 0 {
            return 0;
        }
        let parent = parent as usize;
        for &u in nodes.iter() {
            if u != parent && linked[v][u] && !linked[parent][u] {
                return 0;
            }
        }
        if degree[parent] == degree[v] {
            ways = 2;
        }
    }
    ways
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(seed: &mut i64) -> Vec<Vec<i32>> {
    let k: usize = 500;
    let mut labels: Vec<i32> = (1..=500).collect();
    for i in 0..k {
        let j = i + (next_random(seed) % (500 - i as i64)) as usize;
        labels.swap(i, j);
    }
    let mut have = vec![vec![false; k]; k];
    let mut parent = vec![-1i64; k];
    for i in 1..k {
        let ii = i as i64;
        parent[i] = if next_random(seed) % 2 == 0 { next_random(seed) % ii } else { ii - 1 - next_random(seed) % ii.min(4) };
    }
    for i in 1..k {
        let mut a = parent[i];
        while a >= 0 {
            have[i][a as usize] = true;
            have[a as usize][i] = true;
            a = parent[a as usize];
        }
    }
    let mode = next_random(seed) % 3;
    let i = (next_random(seed) % k as i64) as usize;
    let j = (next_random(seed) % k as i64) as usize;
    if i != j && mode > 0 {
        have[i][j] = mode == 2;
        have[j][i] = mode == 2;
    }
    let mut pairs = Vec::new();
    for i in 0..k {
        for j in i + 1..k {
            if have[i][j] {
                pairs.push(vec![labels[i].min(labels[j]), labels[i].max(labels[j])]);
            }
        }
    }
    pairs
}

fn main() {
    let count = 50;
    let rounds: i64 = 50;
    let mut seed: i64 = 1719;
    let problems: Vec<Vec<Vec<i32>>> = (0..count).map(|_| draw(&mut seed)).collect();
    let pairs: usize = problems.iter().map(|p| p.len()).sum();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for p in problems.iter() {
            let answer = check_ways(p) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} problems of 500 nodes, {} pairs, {} rounds: answers sum to {}, checksum {}", count, pairs, rounds, sum, check);
}
