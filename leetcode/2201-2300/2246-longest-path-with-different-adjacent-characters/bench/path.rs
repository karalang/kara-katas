// LeetCode #2246: Longest Path With Different Adjacent Characters -- the
// benchmark's Rust mirror of path.kara: child lists, breadth-first order
// taken back to front, each node's two longest chains through children
// of another letter.

fn longest_path(parent: &[i64], s: &[u8]) -> i64 {
    let n = parent.len();
    let mut children: Vec<Vec<usize>> = vec![Vec::new(); n];
    for v in 1..n {
        children[parent[v] as usize].push(v);
    }
    let mut order: Vec<usize> = vec![0];
    let mut next = 0;
    while next < order.len() {
        let v = order[next];
        next += 1;
        for &c in &children[v] {
            order.push(c);
        }
    }
    let mut down = vec![1i64; n];
    let mut best = 1;
    for &v in order.iter().rev() {
        let mut first = 0;
        let mut second = 0;
        for &c in &children[v] {
            if s[c] == s[v] {
                continue;
            }
            if down[c] > first {
                second = first;
                first = down[c];
            } else if down[c] > second {
                second = down[c];
            }
        }
        down[v] = first + 1;
        best = best.max(first + second + 1);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let alphabet = b"abcdefghijklmnopqrstuvwxyz";
    let mut seed = 2246i64;
    let mut check = 0i64;
    for _ in 0..40 {
        let mut parent = vec![-1i64; 100000];
        for v in 1..100000 {
            parent[v] = wide_random(&mut seed) % v as i64;
        }
        let s: Vec<u8> = (0..100000).map(|_| alphabet[(next_random(&mut seed) % 26) as usize]).collect();
        check = (check * 31 + longest_path(&parent, &s)) % 1000000007;
    }
    println!("40 trees of 100000 nodes: checksum {}", check);
}
