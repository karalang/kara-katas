// LeetCode 797 — All Paths From Source to Target: the bench, in Rust.
// Mirrors all_paths_source_target.kara: a depth first search keeping the
// path so far, cloning it at node n - 1.

fn all_paths_source_target(graph: &Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let mut paths: Vec<Vec<i64>> = Vec::new();
    let mut path: Vec<i64> = vec![0];
    walk(graph, 0, &mut path, &mut paths);
    paths
}

fn walk(graph: &Vec<Vec<i64>>, node: i64, path: &mut Vec<i64>, paths: &mut Vec<Vec<i64>>) {
    if node == graph.len() as i64 - 1 {
        paths.push(path.clone());
        return;
    }
    for &next in graph[node as usize].iter() {
        path.push(next);
        walk(graph, next, path, paths);
        path.pop();
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 15;
    let mut seed = 797;
    let mut graphs: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..1024 {
        let mut order: Vec<i64> = vec![0];
        for i in 1..n - 1 {
            order.push(i);
        }
        for i in 2..n - 1 {
            let j = 1 + next_random(&mut seed) % i;
            order.swap(i as usize, j as usize);
        }
        order.push(n - 1);
        let chance = 1 + next_random(&mut seed) % 4;
        let mut graph: Vec<Vec<i64>> = vec![Vec::new(); n as usize];
        for a in 0..n as usize {
            for b in a + 1..n as usize {
                if next_random(&mut seed) % 5 < chance {
                    graph[order[a] as usize].push(order[b]);
                }
            }
        }
        graphs.push(graph);
    }
    let rounds: i64 = 40960;
    let (mut count, mut nodes, mut check) = (0i64, 0i64, 0i64);
    for r in 0..rounds {
        let paths = all_paths_source_target(&graphs[(r % 1024) as usize]);
        count += paths.len() as i64;
        for path in paths.iter() {
            nodes += path.len() as i64;
            let mut h = 0i64;
            for &v in path.iter() {
                h = (h * 31 + v + 1) % 1000000007;
            }
            check = (check + h) % 1000000007;
        }
    }
    println!("{rounds} graphs: {count} paths through {nodes} nodes, checksum {check}");
}
