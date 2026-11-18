// LeetCode #1615: Maximal Network Rank -- the bench in Rust, mirroring
// rank.kara: each city's degree and a table of which pairs share a road,
// then every pair's rank.

fn maximal_network_rank(n: i32, roads: &[Vec<i32>]) -> i32 {
    let n = n as usize;
    let mut degree = vec![0; n];
    let mut joined = vec![vec![false; n]; n];
    for road in roads {
        let (a, b) = (road[0] as usize, road[1] as usize);
        degree[a] += 1;
        degree[b] += 1;
        joined[a][b] = true;
        joined[b][a] = true;
    }
    let mut best = 0;
    for a in 0..n {
        for b in a + 1..n {
            let rank = degree[a] + degree[b] - if joined[a][b] { 1 } else { 0 };
            best = best.max(rank);
        }
    }
    best
}

fn main() {
    let mut seed: i64 = 1615;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let n = 100;
    let mut networks: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..2000 {
        let mut roads = Vec::new();
        for a in 0..n {
            for b in a + 1..n {
                if next_random() % 4 == 0 {
                    roads.push(vec![a, b]);
                }
            }
        }
        networks.push(roads);
    }
    let mut check: i64 = 0;
    let mut roads_seen = 0;
    for roads in &networks {
        check = (check * 31 + maximal_network_rank(n, roads) as i64 + 1) % 1000000007;
        roads_seen += roads.len();
    }
    println!("2000 networks of 100 cities: {roads_seen} roads, checksum {check}");
}
