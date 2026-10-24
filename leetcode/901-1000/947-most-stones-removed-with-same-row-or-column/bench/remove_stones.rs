// Benchmark: LeetCode #947 Most Stones Removed with Same Row or Column --
// the ★ arm, rows and columns joined, on sets of 1000 stones, LeetCode's
// largest. Mirrors remove_stones.kara, .c, .py and go-seq/.

use std::collections::HashSet;

fn find_line(parent: &mut [i64], v: i64) -> i64 {
    let mut x = v;
    while parent[x as usize] != x {
        parent[x as usize] = parent[parent[x as usize] as usize];
        x = parent[x as usize];
    }
    x
}

fn remove_stones(stones: &[Vec<i64>]) -> i64 {
    let mut parent = vec![-1i64; 20002];
    let mut groups = 0;
    for s in stones {
        let row = s[0];
        let col = 10001 + s[1];
        if parent[row as usize] < 0 {
            parent[row as usize] = row;
            groups += 1;
        }
        if parent[col as usize] < 0 {
            parent[col as usize] = col;
            groups += 1;
        }
        let a = find_line(&mut parent, row);
        let b = find_line(&mut parent, col);
        if a != b {
            parent[a as usize] = b;
            groups -= 1;
        }
    }
    stones.len() as i64 - groups
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n) = (1000, 20, 1000);
    let mut seed = 947;
    let mut sets: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let side = 200 + next_random(&mut seed) % 1801;
        let mut taken: HashSet<i64> = HashSet::new();
        let mut stones: Vec<Vec<i64>> = Vec::new();
        while stones.len() < n {
            let x = next_random(&mut seed) % side;
            let y = next_random(&mut seed) % side;
            if taken.insert(x * 10001 + y) {
                stones.push(vec![x, y]);
            }
        }
        sets.push(stones);
    }
    let mut total = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let m = remove_stones(&sets[(r + i) % count]);
            total += m;
            check = (check * 1000003 + m) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} sets of {n} stones: {total} removed, checksum {check}");
}
