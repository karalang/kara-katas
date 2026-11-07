// LeetCode #1059: All Paths from Source Lead to Destination -- the
// benchmark, the same algorithm as paths.kara.

const UNSEEN: i64 = 0;
const ON_PATH: i64 = 1;
const DONE: i64 = 2;

fn leads_to_destination(n: i64, edges: &[(i64, i64)], source: i64, destination: i64) -> bool {
    let mut adj: Vec<Vec<i64>> = vec![Vec::new(); n as usize];
    for &(u, v) in edges {
        adj[u as usize].push(v);
    }
    let mut state = vec![UNSEEN; n as usize];
    let mut stack: Vec<(i64, i64)> = vec![(source, 0)];
    state[source as usize] = ON_PATH;
    while !stack.is_empty() {
        let top = stack.len() - 1;
        let (u, next) = stack[top];
        if adj[u as usize].is_empty() && u != destination {
            return false;
        }
        if next == adj[u as usize].len() as i64 {
            state[u as usize] = DONE;
            stack.pop();
            continue;
        }
        stack[top] = (u, next + 1);
        let v = adj[u as usize][next as usize];
        if state[v as usize] == ON_PATH {
            return false;
        }
        if state[v as usize] == UNSEEN {
            state[v as usize] = ON_PATH;
            stack.push((v, 0));
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaning_graph(n: i64, per_node: i64, back: i64, seed: &mut i64) -> Vec<(i64, i64)> {
    let mut edges = Vec::new();
    for u in 0..n - 1 {
        let k = next_random(seed) % (per_node + 1);
        for _ in 0..k {
            let span = (n - 1 - u).min(20);
            edges.push((u, u + 1 + next_random(seed) % span));
        }
        if k == 0 && next_random(seed) % 4 != 0 {
            edges.push((u, n - 1));
        }
        if next_random(seed) % back == 0 {
            edges.push((u, next_random(seed) % (u + 1)));
        }
    }
    edges
}

fn main() {
    let mut seed = 1059i64;
    let n = 2000i64;
    let mut graphs: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..20 {
        graphs.push(leaning_graph(n, 2, 1000, &mut seed));
    }
    let mut calls = 0i64;
    let mut yes = 0i64;
    let mut check = 0i64;
    for edges in &graphs {
        for source in 0..n {
            let answer = leads_to_destination(n, edges, source, n - 1);
            if answer {
                yes += 1;
            }
            check = (check * 31 + if answer { 7 + source % 13 } else { 3 }) % 1000000007;
            calls += 1;
        }
    }
    println!("{} calls: {} lead, checksum {}", calls, yes, check);
}
