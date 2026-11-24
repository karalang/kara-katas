// LeetCode #1334 bench, Rust mirror of the Kāra bench: the ★ arm on 10
// maps of 100 cities built once, then 30 passes, each setting one road's
// weight of every map and the threshold from the checksum so far,
// answering every map.

fn find_the_city(n: i32, edges: &[Vec<i32>], distance_threshold: i32) -> i32 {
    let n = n as usize;
    let far: i64 = 1000000000;
    let mut dist: Vec<Vec<i64>> = vec![vec![far; n]; n];
    for i in 0..n {
        dist[i][i] = 0;
    }
    for e in edges.iter() {
        dist[e[0] as usize][e[1] as usize] = e[2] as i64;
        dist[e[1] as usize][e[0] as usize] = e[2] as i64;
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
    let mut best = 0;
    let mut fewest = n + 1;
    for i in 0..n {
        let near = (0..n).filter(|&j| j != i && dist[i][j] <= distance_threshold as i64).count();
        if near <= fewest {
            fewest = near;
            best = i;
        }
    }
    best as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 100i64;
    let mut seed = 1334i64;
    let mut maps: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..10 {
        let mut edges: Vec<Vec<i32>> = Vec::new();
        for a in 0..n {
            for b in a + 1..n {
                if next_random(&mut seed) % 2 == 0 {
                    edges.push(vec![a as i32, b as i32, (1 + next_random(&mut seed) % 10000) as i32]);
                }
            }
        }
        maps.push(edges);
    }
    let mut check: i64 = 0;
    for pass in 0..30i64 {
        let threshold = (200 + check % 800) as i32;
        for t in 0..10 {
            let at = (check % maps[t].len() as i64) as usize;
            maps[t][at][2] = (1 + check / 3 % 10000) as i32;
            let city = find_the_city(n as i32, &maps[t], threshold);
            check = (check * 31 + city as i64 + pass) % 1000000007;
        }
    }
    println!("30 passes over 10 maps of 100 cities: checksum {}", check);
}
