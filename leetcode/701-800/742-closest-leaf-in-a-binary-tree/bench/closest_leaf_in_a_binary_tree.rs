// LeetCode #742: Closest Leaf in a Binary Tree -- breadth first from k.
// Benchmark mirror of the Kara star arm: treat the tree as an undirected
// graph, each node's neighbours its children and its parent, and search
// outward from k a layer at a time; the first layer holding a leaf holds
// the nearest ones, and the smallest value of those is returned.

struct Node {
    val: i64,
    left: i64,
    right: i64,
}

fn find_closest_leaf(nodes: &Vec<Node>, k: i64) -> i64 {
    let n = nodes.len();
    let mut parent: Vec<i64> = Vec::new();
    let mut start = 0;
    for i in 0..n {
        parent.push(-1);
        if nodes[i].val == k {
            start = i;
        }
    }
    for i in 0..n {
        if nodes[i].left != -1 {
            parent[nodes[i].left as usize] = i as i64;
        }
        if nodes[i].right != -1 {
            parent[nodes[i].right as usize] = i as i64;
        }
    }
    let mut seen: Vec<bool> = Vec::new();
    for _ in 0..n {
        seen.push(false);
    }
    seen[start] = true;
    let mut layer: Vec<usize> = vec![start];
    loop {
        let mut best = -1;
        for x in layer.iter() {
            let node = &nodes[*x];
            if node.left == -1 && node.right == -1 && (best == -1 || node.val < best) {
                best = node.val;
            }
        }
        if best != -1 {
            return best;
        }
        let mut next: Vec<usize> = Vec::new();
        for x in layer.iter() {
            for y in [nodes[*x].left, nodes[*x].right, parent[*x]] {
                if y != -1 && !seen[y as usize] {
                    seen[y as usize] = true;
                    next.push(y as usize);
                }
            }
        }
        layer = next;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 742;
    let n: i64 = 1000;
    let mut values: Vec<i64> = (1..n + 1).collect();
    for i in 0..n {
        let j = i + next_random(&mut seed) % (n - i);
        values.swap(i as usize, j as usize);
    }
    let mut nodes: Vec<Node> = Vec::new();
    nodes.push(Node { val: values[0], left: -1, right: -1 });
    for i in 1..n {
        loop {
            let p = (next_random(&mut seed) % i) as usize;
            if next_random(&mut seed) % 2 == 0 {
                if nodes[p].left == -1 {
                    nodes[p].left = i;
                    break;
                }
            } else if nodes[p].right == -1 {
                nodes[p].right = i;
                break;
            }
        }
        nodes.push(Node { val: values[i as usize], left: -1, right: -1 });
    }
    let mut total: i64 = 0;
    for _ in 0..60 {
        let a = (next_random(&mut seed) % n) as usize;
        let b = (next_random(&mut seed) % n) as usize;
        let t = nodes[a].val;
        nodes[a].val = nodes[b].val;
        nodes[b].val = t;
        for k in 1..n + 1 {
            total += find_closest_leaf(&nodes, k);
        }
    }
    println!("60 rounds of 1000 queries on a 1000-node tree: answers sum to {}", total);
}
