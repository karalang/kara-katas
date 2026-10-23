// LeetCode #904: Fruit Into Baskets -- bench program, Rust.
//
// The last two types and the last run, over one row of 1,000,000 trees
// built once, of 3 types in runs of 1 to 50 trees. Each round finds the
// most fruit, folds it into a checksum and changes one tree's type.

fn total_fruit(fruits: &[i64]) -> i64 {
    let mut last: i64 = -1;
    let mut before: i64 = -1;
    let mut run: i64 = 0;
    let mut current: i64 = 0;
    let mut best: i64 = 0;
    for &f in fruits.iter() {
        if f == last || f == before {
            current += 1;
        } else {
            current = run + 1;
        }
        if f == last {
            run += 1;
        } else {
            run = 1;
            before = last;
            last = f;
        }
        best = best.max(current);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let trees: usize = 1000000;
    let rounds: i64 = 240;
    let mut seed: i64 = 904;
    let mut fruits: Vec<i64> = Vec::new();
    while fruits.len() < trees {
        let f = next_random(&mut seed) % 3;
        let r = 1 + next_random(&mut seed) % 50;
        for _ in 0..r {
            if fruits.len() < trees {
                fruits.push(f);
            }
        }
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for round in 0..rounds {
        let got = total_fruit(&fruits);
        total += got;
        check = (check * 31 + got) % 1000000007;
        fruits[(round as usize) * 7919 % trees] = next_random(&mut seed) % 3;
    }
    println!("{} rounds over {} trees: answers summing to {}, checksum {}", rounds, trees, total, check);
}
