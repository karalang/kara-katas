// Benchmark for #404: mirror of sum_of_left_leaves.kara (recursion that
// knows which side it came from), over the same index pool.

struct Node {
    val: i64,
    left: i64,
    right: i64,
}

fn visit(nodes: &[Node], node: i64, is_left: bool) -> i64 {
    if node == -1 {
        return 0;
    }
    let at = &nodes[node as usize];
    if at.left == -1 && at.right == -1 {
        return if is_left { at.val } else { 0 };
    }
    visit(nodes, at.left, true) + visit(nodes, at.right, false)
}

fn sum_of_left_leaves(nodes: &[Node]) -> i64 {
    if nodes.is_empty() {
        return 0;
    }
    visit(nodes, 0, false)
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let trees = 50;
    let n: i64 = 30000;
    let rounds = 50;
    let mut seed: i64 = 404;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..trees {
        let mut nodes: Vec<Node> = Vec::new();
        nodes.push(Node { val: step(&mut seed) % 201 - 100, left: -1, right: -1 });
        for i in 1..n {
            let mut p = (step(&mut seed) % i) as usize;
            let mut side = 1 + step(&mut seed) % 2;
            while (side == 1 && nodes[p].left != -1) || (side == 2 && nodes[p].right != -1) {
                p = (step(&mut seed) % i) as usize;
                side = 1 + step(&mut seed) % 2;
            }
            nodes.push(Node { val: step(&mut seed) % 201 - 100, left: -1, right: -1 });
            if side == 1 {
                nodes[p].left = i;
            } else {
                nodes[p].right = i;
            }
        }
        for r in 0..rounds {
            nodes[r as usize].val += 1;
            let s = sum_of_left_leaves(&nodes);
            total += s;
            checksum = (checksum * 31 + s + 10000000 + r) % 1000000007;
        }
    }
    println!("{} trees of {} nodes, {} rounds: total {}, checksum {}", trees, n, rounds, total, checksum);
}
