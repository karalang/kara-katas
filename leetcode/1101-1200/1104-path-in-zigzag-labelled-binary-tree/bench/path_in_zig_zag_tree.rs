// LeetCode #1104: Path In Zigzag Labelled Binary Tree -- the bench in
// Rust: the ★ arm (walking up, each parent half the label's mirror in its
// row) over every label from 1 to 10^6 in a different order each of 8
// rounds.

fn path_in_zig_zag_tree(label: i64) -> Vec<i64> {
    let mut depth = 1;
    while (1i64 << depth) <= label {
        depth += 1;
    }
    let mut path: Vec<i64> = Vec::new();
    let mut node = label;
    while depth > 0 {
        path.push(node);
        let (start, end) = (1i64 << (depth - 1), (1i64 << depth) - 1);
        node = (start + end - node) / 2;
        depth -= 1;
    }
    path.reverse();
    path
}

fn main() {
    let mut nodes = 0i64;
    let mut check = 0i64;
    for round in 0..8i64 {
        for i in 0..1000000i64 {
            let label = (i * 7919 + round * 104729) % 1000000 + 1;
            let path = path_in_zig_zag_tree(label);
            nodes += path.len() as i64;
            check = (check * 31 + path[path.len() / 2]) % 1000000007;
        }
    }
    println!("8 rounds over the labels 1 to 10^6: {} nodes on their paths, checksum {}", nodes, check);
}
