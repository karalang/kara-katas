// LeetCode #1617: Count Subtrees With Max Distance Between Cities -- the
// bench in Rust, mirroring subtrees.kara: all pair distances by
// Floyd-Warshall, then every mask of two or more cities that holds one
// road fewer than it has cities, its largest distance counted.

fn count_subgraphs_for_each_diameter(n: i32, edges: &[Vec<i32>]) -> Vec<i32> {
    let n = n as usize;
    let far = n as i64 + 1;
    let mut dist = vec![vec![far; n]; n];
    for i in 0..n {
        dist[i][i] = 0;
    }
    let mut ends: Vec<(usize, usize)> = Vec::new();
    for e in edges {
        let (a, b) = ((e[0] - 1) as usize, (e[1] - 1) as usize);
        dist[a][b] = 1;
        dist[b][a] = 1;
        ends.push((a, b));
    }
    for k in 0..n {
        for i in 0..n {
            for j in 0..n {
                if dist[i][k] + dist[k][j] < dist[i][j] {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }
    let mut answer = vec![0i32; n - 1];
    for mask in 1i64..(1 << n) {
        let size = mask.count_ones() as usize;
        if size < 2 {
            continue;
        }
        let roads = ends.iter().filter(|&&(a, b)| mask >> a & 1 == 1 && mask >> b & 1 == 1).count();
        if roads != size - 1 {
            continue;
        }
        let mut widest = 0;
        for i in 0..n {
            if mask >> i & 1 == 1 {
                for j in i + 1..n {
                    if mask >> j & 1 == 1 {
                        widest = widest.max(dist[i][j]);
                    }
                }
            }
        }
        answer[widest as usize - 1] += 1;
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn random_tree(n: i64, seed: &mut i64) -> Vec<Vec<i32>> {
    let mut name: Vec<i32> = (1..=n).map(|c| c as i32).collect();
    for i in (1..n).rev() {
        let j = next_random(seed) % (i + 1);
        name.swap(i as usize, j as usize);
    }
    let mut edges = Vec::new();
    for c in 1..n {
        let p = next_random(seed) % c;
        edges.push(vec![name[c as usize], name[p as usize]]);
    }
    edges
}

fn main() {
    let mut seed = 1617;
    let trees: Vec<Vec<Vec<i32>>> = (0..400).map(|_| random_tree(15, &mut seed)).collect();
    let (mut check, mut subtrees) = (0i64, 0i64);
    for edges in &trees {
        for &x in &count_subgraphs_for_each_diameter(15, edges) {
            check = mix(check, x as i64);
            subtrees += x as i64;
        }
    }
    println!("400 trees of 15 cities: {subtrees} subtrees, checksum {check}");
}
