// LeetCode #2876: Count Visited Nodes in a Directed Graph -- the bench,
// as visited.kara: 20 graphs of 10^5 nodes, each answered 20 times by
// the peeling arm.

fn count_visited_nodes(edges: &[usize]) -> Vec<i64> {
    let n = edges.len();
    let mut incoming = vec![0i64; n];
    for &e in edges {
        incoming[e] += 1;
    }
    let mut peeled: Vec<usize> = (0..n).filter(|&u| incoming[u] == 0).collect();
    let mut head = 0;
    while head < peeled.len() {
        let w = edges[peeled[head]];
        head += 1;
        incoming[w] -= 1;
        if incoming[w] == 0 {
            peeled.push(w);
        }
    }
    let mut answer = vec![0i64; n];
    for start in 0..n {
        if incoming[start] > 0 && answer[start] == 0 {
            let mut cycle = vec![start];
            let mut u = edges[start];
            while u != start {
                cycle.push(u);
                u = edges[u];
            }
            for &v in &cycle {
                answer[v] = cycle.len() as i64;
            }
        }
    }
    for &u in peeled.iter().rev() {
        answer[u] = answer[edges[u]] + 1;
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (20, 20usize, 100000usize);
    let mut seed = 2876;
    let mut graphs: Vec<Vec<usize>> = Vec::new();
    for c in 0..count {
        let edges: Vec<usize> = (0..n as i64)
            .map(|i| {
                let e = if c % 2 == 1 {
                    (i + next_random(&mut seed) % 5 + 1) % n as i64
                } else {
                    (i + wide(&mut seed) % (n as i64 - 1) + 1) % n as i64
                };
                e as usize
            })
            .collect();
        graphs.push(edges);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for edges in graphs.iter() {
            let counts = count_visited_nodes(edges);
            total += counts.iter().sum::<i64>();
            check = (check * 31 + counts[r] + counts[n - 1 - r]) % 1000000007;
        }
    }
    println!("{count} graphs of {n}, {rounds} rounds: visits total {total}, checksum {check}");
}
