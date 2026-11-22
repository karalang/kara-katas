// LeetCode #2858: Minimum Edge Reversals So Every Node Is Reachable --
// the bench: the ★ arm over 20 random trees of 10^5 nodes, LeetCode's
// most, every other one deep, labels shuffled and each edge pointing
// either way, all drawn first, then each answered 5 times.

fn min_edge_reversals(n: usize, edges: &[Vec<usize>]) -> Vec<i64> {
    let mut adj: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for e in edges.iter() {
        adj[e[0]].push((e[1], 0));
        adj[e[1]].push((e[0], 1));
    }
    let mut parent: Vec<i64> = vec![-1; n];
    let mut cost: Vec<i64> = vec![0; n];
    let mut order: Vec<usize> = Vec::new();
    let mut stack = vec![0usize];
    parent[0] = 0;
    let mut root = 0;
    while let Some(u) = stack.pop() {
        order.push(u);
        for &(v, w) in adj[u].iter() {
            if parent[v] == -1 {
                parent[v] = u as i64;
                cost[v] = w;
                root += w;
                stack.push(v);
            }
        }
    }
    let mut answer: Vec<i64> = vec![0; n];
    answer[0] = root;
    for &u in order.iter().skip(1) {
        answer[u] = answer[parent[u] as usize] + if cost[u] == 0 { 1 } else { -1 };
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn tree(n: usize, deep: bool, seed: &mut i64) -> Vec<Vec<usize>> {
    let mut label: Vec<usize> = (0..n).collect();
    for i in (1..n).rev() {
        let j = (wide(seed) % (i as i64 + 1)) as usize;
        label.swap(i, j);
    }
    let mut edges: Vec<Vec<usize>> = Vec::new();
    for i in 1..n {
        let p = if deep { i - 1 - (next_random(seed) % i.min(3) as i64) as usize } else { (wide(seed) % i as i64) as usize };
        if next_random(seed) % 2 == 0 {
            edges.push(vec![label[p], label[i]]);
        } else {
            edges.push(vec![label[i], label[p]]);
        }
    }
    edges
}

fn main() {
    let count = 20;
    let rounds = 5;
    let n = 100000;
    let mut seed = 2858;
    let trees: Vec<Vec<Vec<usize>>> = (0..count).map(|c| tree(n, c % 2 == 1, &mut seed)).collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for edges in trees.iter() {
            let answer = min_edge_reversals(n, edges);
            for &a in answer.iter() {
                total += a;
                check = (check * 31 + a + r) % 1000000007;
            }
        }
    }
    println!("{count} trees of {n}, {rounds} rounds: answers sum to {total}, checksum {check}");
}
