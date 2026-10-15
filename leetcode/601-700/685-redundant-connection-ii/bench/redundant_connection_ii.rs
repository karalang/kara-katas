// LeetCode #685: Redundant Connection II -- union-find and two
// candidates. Bench.
//
// 100 random rooted trees of 20,000 vertices, each with one more directed
// edge, are built once; then 30 rounds answer every graph.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut v = x;
    while parent[v as usize] != v {
        parent[v as usize] = parent[parent[v as usize] as usize];
        v = parent[v as usize];
    }
    v
}

fn find_redundant_directed_connection(edges: &[(i64, i64)]) -> (i64, i64) {
    let n = edges.len();
    let mut into: Vec<i64> = vec![-1; n + 1];
    let mut first: i64 = -1;
    let mut second: i64 = -1;
    for (i, &(_, b)) in edges.iter().enumerate() {
        if into[b as usize] == -1 {
            into[b as usize] = i as i64;
        } else {
            first = into[b as usize];
            second = i as i64;
        }
    }
    let mut parent: Vec<i64> = (0..=n as i64).collect();
    for (i, &(a, b)) in edges.iter().enumerate() {
        if i as i64 != second {
            let ra = find(&mut parent, a);
            let rb = find(&mut parent, b);
            if ra == rb {
                return if first == -1 { (a, b) } else { edges[first as usize] };
            }
            parent[rb as usize] = ra;
        }
    }
    edges[second as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 100;
    let n: i64 = 20000;
    let rounds: i64 = 30;
    let mut seed: i64 = 685;
    let mut graphs: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..count {
        let mut name: Vec<i64> = (1..=n).collect();
        let mut i = n - 1;
        while i > 0 {
            let j = next_random(&mut seed) % (i + 1);
            name.swap(i as usize, j as usize);
            i -= 1;
        }
        let mut up: Vec<i64> = vec![0; n as usize + 1];
        let mut edges: Vec<(i64, i64)> = Vec::new();
        for v in 1..n {
            let a = name[(next_random(&mut seed) % v) as usize];
            up[name[v as usize] as usize] = a;
            edges.push((a, name[v as usize]));
        }
        loop {
            let a = 1 + next_random(&mut seed) % n;
            let b = 1 + next_random(&mut seed) % n;
            if a != b && up[b as usize] != a {
                edges.push((a, b));
                break;
            }
        }
        let mut k = n - 1;
        while k > 0 {
            let j = next_random(&mut seed) % (k + 1);
            edges.swap(k as usize, j as usize);
            k -= 1;
        }
        graphs.push(edges);
    }
    let mut sum: i64 = 0;
    for r in 0..rounds {
        for c in 0..count as usize {
            let (a, b) = find_redundant_directed_connection(&graphs[c]);
            sum = (sum * 31 + a * 20011 + b + r) % 1000000007;
        }
    }
    println!("{} graphs answered, checksum {}", count * rounds, sum);
}
