// LeetCode #1042: Flower Planting With No Adjacent -- bench, Rust mirror
// of garden_no_adj.kara (greedy over the gardens in order).

fn garden_no_adj(n: i64, paths: &[(i64, i64)]) -> Vec<i64> {
    let mut neighbors: Vec<Vec<i64>> = Vec::new();
    for _ in 0..n {
        neighbors.push(Vec::new());
    }
    for &(x, y) in paths {
        neighbors[(x - 1) as usize].push(y - 1);
        neighbors[(y - 1) as usize].push(x - 1);
    }
    let mut answer = vec![0i64; n as usize];
    for garden in 0..n as usize {
        let mut taken = [false; 5];
        for &other in &neighbors[garden] {
            taken[answer[other as usize] as usize] = true;
        }
        let mut flower = 1;
        while taken[flower] {
            flower += 1;
        }
        answer[garden] = flower as i64;
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_paths(n: i64, tries: i64, seed: &mut i64) -> Vec<(i64, i64)> {
    let mut joined: Vec<Vec<i64>> = vec![Vec::new(); n as usize];
    let mut paths = Vec::new();
    for _ in 0..tries {
        let x = next_random(seed) % n;
        let y = next_random(seed) % n;
        let (xu, yu) = (x as usize, y as usize);
        if x != y && joined[xu].len() < 3 && joined[yu].len() < 3 && !joined[xu].contains(&y) {
            joined[xu].push(y);
            joined[yu].push(x);
            paths.push((x + 1, y + 1));
        }
    }
    paths
}

fn main() {
    let count = 10;
    let n = 10000;
    let rounds = 100;
    let mut seed = 1042;
    let mut gardens = Vec::new();
    for _ in 0..count {
        gardens.push(random_paths(n, 4 * n, &mut seed));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for paths in &gardens {
            let answer = garden_no_adj(n, paths);
            let mut sum = 0;
            for &flower in &answer {
                sum += flower;
            }
            total += sum;
            check = (check * 131 + sum) % 1000000007;
        }
    }
    println!("{count} gardens of {n} plots, {rounds} rounds: types sum to {total}, checksum {check}");
}
