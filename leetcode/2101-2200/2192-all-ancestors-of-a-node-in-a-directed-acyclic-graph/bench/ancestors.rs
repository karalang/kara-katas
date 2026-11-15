// benchmark's Rust mirror of ancestors.kara (LeetCode #2192, the ★ arm):
// a walk down from every node by a stack.

fn get_ancestors(n: usize, edges: &[[usize; 2]]) -> Vec<Vec<usize>> {
    let mut children: Vec<Vec<usize>> = vec![Vec::new(); n];
    for e in edges {
        children[e[0]].push(e[1]);
    }
    let mut ancestors: Vec<Vec<usize>> = vec![Vec::new(); n];
    for start in 0..n {
        let mut seen = vec![false; n];
        seen[start] = true;
        let mut stack = vec![start];
        while let Some(u) = stack.pop() {
            for &v in &children[u] {
                if !seen[v] {
                    seen[v] = true;
                    ancestors[v].push(start);
                    stack.push(v);
                }
            }
        }
    }
    ancestors
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_dag(seed: &mut i64) -> Vec<[usize; 2]> {
    let mut order: Vec<usize> = (0..1000).collect();
    for i in (1..1000).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        order.swap(i, j);
    }
    let mut edges = Vec::new();
    while edges.len() < 2000 {
        let a = (next_random(seed) % 1000) as usize;
        let b = (next_random(seed) % 1000) as usize;
        if a < b {
            edges.push([order[a], order[b]]);
        } else if b < a {
            edges.push([order[b], order[a]]);
        }
    }
    edges
}

fn main() {
    let mut seed = 2192;
    let dags: Vec<Vec<[usize; 2]>> = (0..20).map(|_| random_dag(&mut seed)).collect();
    let mut check: i64 = 0;
    for r in 0..2000 {
        for list in get_ancestors(1000, &dags[r % 20]) {
            check = (check * 31 + list.len() as i64) % 1000000007;
            for a in list {
                check = (check * 31 + a as i64 + 1) % 1000000007;
            }
        }
    }
    println!("2000 solves: checksum {}", check);
}
