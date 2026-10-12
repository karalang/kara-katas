// Benchmark for #428: mirror of codec.kara (preorder with child
// counts). The split copies each word into its own String, as the Kāra
// program's split does.
struct Node {
    val: i64,
    children: Vec<Node>,
}

fn write(node: &Node, out: &mut String) {
    if !out.is_empty() {
        out.push(' ');
    }
    out.push_str(&format!("{} {}", node.val, node.children.len()));
    for child in &node.children {
        write(child, out);
    }
}

fn serialize(root: &Option<Node>) -> String {
    let mut out = String::new();
    if let Some(node) = root {
        write(node, &mut out);
    }
    out
}

fn read(words: &[String], at: &mut usize) -> Node {
    let val: i64 = words[*at].parse().unwrap();
    let count: i64 = words[*at + 1].parse().unwrap();
    *at += 2;
    let mut children = Vec::new();
    for _ in 0..count {
        children.push(read(words, at));
    }
    Node { val, children }
}

fn deserialize(data: &str) -> Option<Node> {
    if data.is_empty() {
        return None;
    }
    let words: Vec<String> = data.split(' ').map(String::from).collect();
    let mut at = 0;
    Some(read(&words, &mut at))
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

fn total(node: &Node) -> i64 {
    let mut sum = node.val;
    for child in &node.children {
        sum += total(child);
    }
    sum
}

fn main() {
    let n: i64 = 10000;
    let rounds: i64 = std::env::args().nth(1).map_or(100, |s| s.parse().unwrap());
    let mut seed: i64 = 428;
    let mut chars: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let reach = 1 + step(&mut seed) % 1000;
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
        let tree = Some(build_random(0, &vals, &kids));
        let text = serialize(&tree);
        let back = deserialize(&text).expect("the tree is not empty");
        chars += text.len() as i64;
        checksum = (checksum * 31 + text.len() as i64 + total(&back)) % 1000000007;
    }
    println!("{} rounds of {} nodes: {} characters, checksum {}", rounds, n, chars, checksum);
}
