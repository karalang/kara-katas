// LeetCode #1519 bench: the ★ arm (counts returned up a recursive walk),
// as labels.kara.

fn walk(node: usize, parent: usize, adjacent: &Vec<Vec<usize>>, labels: &[u8], answer: &mut Vec<i64>) -> Vec<i64> {
    let mut counts = vec![0i64; 26];
    for &next in adjacent[node].iter() {
        if next != parent {
            let below = walk(next, node, adjacent, labels, answer);
            for c in 0..26 {
                counts[c] += below[c];
            }
        }
    }
    let mine = (labels[node] - 97) as usize;
    counts[mine] += 1;
    answer[node] = counts[mine];
    counts
}

fn count_sub_trees(n: usize, edges: &[(usize, usize)], labels: &str) -> Vec<i64> {
    let mut adjacent: Vec<Vec<usize>> = vec![Vec::new(); n];
    for &(a, b) in edges {
        adjacent[a].push(b);
        adjacent[b].push(a);
    }
    let mut answer = vec![0i64; n];
    walk(0, usize::MAX, &adjacent, labels.as_bytes(), &mut answer);
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 200000;
    let mut seed = 1519i64;
    let mut edges: Vec<(usize, usize)> = Vec::new();
    for i in 1..n {
        let a = next_random(&mut seed);
        let p = (a * 32768 + next_random(&mut seed)) % i;
        edges.push((p as usize, i as usize));
    }
    let mut labels = String::new();
    for _ in 0..n {
        labels.push((97 + next_random(&mut seed) % 26) as u8 as char);
    }
    let mut check: i64 = 0;
    for _ in 0..5 {
        for &x in count_sub_trees(n as usize, &edges, &labels).iter() {
            check = (check * 31 + x + 1) % 1000000007;
        }
    }
    println!("5 passes over a tree of 200000 nodes: checksum {}", check);
}
