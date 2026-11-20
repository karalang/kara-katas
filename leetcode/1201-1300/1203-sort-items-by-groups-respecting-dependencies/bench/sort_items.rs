// LeetCode #1203 bench, in Rust: the ★ arm (each item in no group given one
// of its own, then Kahn's algorithm over the groups and over the items) on
// four instances of 30000 items drawn once, then 10 rounds over the four,
// each answer folded into a checksum.

fn topo_sort(nodes: usize, edges: &[Vec<usize>]) -> Vec<usize> {
    let mut indegree = vec![0usize; nodes];
    for out in edges {
        for &v in out {
            indegree[v] += 1;
        }
    }
    let mut order: Vec<usize> = (0..nodes).filter(|&v| indegree[v] == 0).collect();
    let mut head = 0;
    while head < order.len() {
        let u = order[head];
        head += 1;
        for &v in &edges[u] {
            indegree[v] -= 1;
            if indegree[v] == 0 {
                order.push(v);
            }
        }
    }
    if order.len() == nodes { order } else { Vec::new() }
}

fn sort_items(n: usize, m: usize, group: &[i64], before_items: &[Vec<usize>]) -> Vec<usize> {
    let mut owner = vec![0usize; n];
    let mut groups = m;
    for i in 0..n {
        if group[i] < 0 {
            owner[i] = groups;
            groups += 1;
        } else {
            owner[i] = group[i] as usize;
        }
    }
    let mut item_edges: Vec<Vec<usize>> = vec![Vec::new(); n];
    let mut group_edges: Vec<Vec<usize>> = vec![Vec::new(); groups];
    for i in 0..n {
        for &b in &before_items[i] {
            item_edges[b].push(i);
            if owner[b] != owner[i] {
                group_edges[owner[b]].push(owner[i]);
            }
        }
    }
    let items = topo_sort(n, &item_edges);
    let ranks = topo_sort(groups, &group_edges);
    if items.is_empty() || ranks.is_empty() {
        return Vec::new();
    }
    let mut members: Vec<Vec<usize>> = vec![Vec::new(); groups];
    for &i in &items {
        members[owner[i]].push(i);
    }
    let mut out = Vec::new();
    for &g in &ranks {
        out.extend_from_slice(&members[g]);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn dependencies(seed: &mut i64, n: usize, most: i64) -> Vec<Vec<usize>> {
    let mut before_items: Vec<Vec<usize>> = vec![Vec::new(); n];
    for i in 1..n {
        for _ in 0..next_random(seed) % (most + 1) {
            let hi = next_random(seed);
            let b = ((hi * 32768 + next_random(seed)) % i as i64) as usize;
            if !before_items[i].contains(&b) {
                before_items[i].push(b);
            }
        }
    }
    before_items
}

fn main() {
    let n = 30000;
    let m = 3000;
    let mut seed = 1203i64;
    let runs: Vec<i64> = (0..n).map(|i| if i % 10 == 0 { -1 } else { (i / 10) as i64 }).collect();
    let loose = dependencies(&mut seed, n, 3);
    let dense = dependencies(&mut seed, n, 6);
    let mut cycle = loose.clone();
    cycle[0].push(n - 1);
    if !cycle[n - 1].contains(&0) {
        cycle[n - 1].push(0);
    }
    let instances = [
        (runs.clone(), loose),
        (runs.clone(), dense),
        (vec![-1i64; n], dependencies(&mut seed, n, 3)),
        (runs, cycle),
    ];
    let mut check: i64 = 0;
    for _ in 0..10 {
        for (group, before_items) in &instances {
            let order = sort_items(n, m, group, before_items);
            check = (check * 131 + order.len() as i64) % 1000000007;
            for &i in &order {
                check = (check * 131 + i as i64 + 1) % 1000000007;
            }
        }
    }
    println!("10 rounds over 4 instances of 30000 items: checksum {check}");
}
