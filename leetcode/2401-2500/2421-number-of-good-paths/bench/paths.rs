// LeetCode #2421: Number of Good Paths -- the bench, the ★ arm: union-find
// over the nodes in order of value, each value's nodes joined to their
// neighbours no larger and then counted by root.

use std::collections::HashMap;

fn find(parent: &mut [usize], x: usize) -> usize {
    let mut x = x;
    while parent[x] != x {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    x
}

fn number_of_good_paths(vals: &[i64], edges: &[(usize, usize)]) -> i64 {
    let n = vals.len();
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    for &(a, b) in edges {
        adj[a].push(b);
        adj[b].push(a);
    }
    let mut parent: Vec<usize> = (0..n).collect();
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by_key(|&i| vals[i]);
    let mut good = n as i64;
    let mut i = 0;
    while i < n {
        let mut j = i;
        while j < n && vals[order[j]] == vals[order[i]] {
            j += 1;
        }
        for t in i..j {
            let u = order[t];
            for &v in &adj[u] {
                if vals[v] <= vals[u] {
                    let ru = find(&mut parent, u);
                    let rv = find(&mut parent, v);
                    parent[ru] = rv;
                }
            }
        }
        let mut count: HashMap<usize, i64> = HashMap::new();
        for t in i..j {
            let root = find(&mut parent, order[t]);
            *count.entry(root).or_insert(0) += 1;
        }
        for &c in count.values() {
            good += c * (c - 1) / 2;
        }
        i = j;
    }
    good
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2421;
    let mut trees: Vec<(Vec<i64>, Vec<(usize, usize)>)> = Vec::new();
    for t in 0..10 {
        let n = 30000;
        let vals: Vec<i64> = (0..n).map(|_| 1 + next_random(&mut seed) % (3 + 1000 * t)).collect();
        let edges: Vec<(usize, usize)> = (1..n).map(|i| ((next_random(&mut seed) % i as i64) as usize, i)).collect();
        trees.push((vals, edges));
    }
    let mut check: i64 = 0;
    for p in 0..20 {
        for (vals, edges) in trees.iter() {
            check = (check * 31 + number_of_good_paths(vals, edges) + p) % 1000000007;
        }
    }
    println!("20 passes over 10 trees of 3 * 10^4 nodes: checksum {}", check);
}
