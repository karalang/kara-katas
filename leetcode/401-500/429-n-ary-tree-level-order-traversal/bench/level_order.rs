// Benchmark for #429: mirror of level_order.kara (breadth first, a
// level at a time). The tree is taken by value and each node's children
// move into the next level, as in the Kāra arm.
struct Node {
    val: i64,
    children: Vec<Node>,
}

fn level_order(root: Option<Node>) -> Vec<Vec<i64>> {
    let mut levels = Vec::new();
    let mut level: Vec<Node> = root.into_iter().collect();
    while !level.is_empty() {
        let mut row = Vec::new();
        let mut next = Vec::new();
        for node in level {
            row.push(node.val);
            for child in node.children {
                next.push(child);
            }
        }
        levels.push(row);
        level = next;
    }
    levels
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn build_random(i: usize, vals: &[i64], kids: &[Vec<usize>]) -> Node {
    let mut children = Vec::new();
    for &k in &kids[i] {
        children.push(build_random(k, vals, kids));
    }
    Node { val: vals[i], children }
}

fn main() {
    let n: i64 = 10000;
    let rounds: i64 = std::env::args().nth(1).map_or(200, |s| s.parse().unwrap());
    let mut seed: i64 = 429;
    let mut rows: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let reach = 10 + step(&mut seed) % 1000;
        let mut vals: Vec<i64> = Vec::new();
        let mut kids: Vec<Vec<usize>> = Vec::new();
        for i in 0..n {
            vals.push(step(&mut seed) % 10001);
            kids.push(Vec::new());
            if i > 0 {
                let back = 1 + step(&mut seed) % i.min(reach);
                kids[(i - back) as usize].push(i as usize);
            }
        }
        let levels = level_order(Some(build_random(0, &vals, &kids)));
        rows += levels.len() as i64;
        for row in &levels {
            checksum = (checksum * 31 + row.len() as i64 * 10007 + row[0] + row[row.len() - 1]) % 1000000007;
        }
    }
    println!("{} rounds of {} nodes: {} levels, checksum {}", rounds, n, rows, checksum);
}
