// Benchmark for #573: Rust mirror of the ★ arm (one pass with the best
// first nut); see min_distance.kara. Each nut is a `Vec<i64>` of two, as
// LeetCode gives it and as the Kāra arm takes it.

fn distance(a: &[i64], b: &[i64]) -> i64 {
    (a[0] - b[0]).abs() + (a[1] - b[1]).abs()
}

fn min_distance(_height: i64, _width: i64, tree: &[i64], squirrel: &[i64], nuts: &[Vec<i64>]) -> i64 {
    let mut total = 0;
    let mut best_saving = i64::MIN;
    for nut in nuts.iter() {
        let to_tree = distance(nut, tree);
        total += 2 * to_tree;
        best_saving = best_saving.max(to_tree - distance(nut, squirrel));
    }
    total - best_saving
}

// ---- benchmark --------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 20;
    let rounds: i64 = 2000;
    let mut seed: i64 = 573;
    let mut trees: Vec<Vec<i64>> = Vec::new();
    let mut squirrels: Vec<Vec<i64>> = Vec::new();
    let mut nut_sets: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let r = next_random(&mut seed) % 100;
        trees.push(vec![r, next_random(&mut seed) % 100]);
        let r = next_random(&mut seed) % 100;
        squirrels.push(vec![r, next_random(&mut seed) % 100]);
        let mut nuts: Vec<Vec<i64>> = Vec::new();
        for _ in 0..5000 {
            let r = next_random(&mut seed) % 100;
            nuts.push(vec![r, next_random(&mut seed) % 100]);
        }
        nut_sets.push(nuts);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let p = ((round * 7 + g) % count) as usize;
            let got = min_distance(100, 100, &trees[p], &squirrels[p], &nut_sets[p]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    println!("{} cases of 5000 nuts, {} rounds: {} steps, checksum {}", count, rounds, total, checksum);
}
