// LeetCode #1791: Find Center of Star Graph -- the bench in Rust, mirroring
// find_center.kara: the node the first two edges share.

fn find_center(edges: &[Vec<i32>]) -> i32 {
    let (a, b) = (edges[0][0], edges[0][1]);
    if a == edges[1][0] || a == edges[1][1] { a } else { b }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1791;
    let mut stars: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..2000 {
        let center = 1 + next_random(&mut seed) % 100;
        let mut edges: Vec<Vec<i32>> = Vec::new();
        for leaf in 1..101 {
            if leaf == center {
                continue;
            }
            if next_random(&mut seed) % 2 == 0 {
                edges.push(vec![center as i32, leaf as i32]);
            } else {
                edges.push(vec![leaf as i32, center as i32]);
            }
        }
        for i in (1..edges.len()).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            edges.swap(i, j);
        }
        stars.push(edges);
    }
    let mut check: i64 = 0;
    for call in 0..20000000i64 {
        let edges = &stars[((check + call) % 2000) as usize];
        check = (check * 41 + find_center(edges) as i64) % 1000000007;
    }
    println!("20000000 calls over 2000 stars: checksum {}", check);
}
