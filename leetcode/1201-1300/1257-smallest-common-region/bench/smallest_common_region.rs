// LeetCode #1257 bench, in Rust: the ★ arm (each region's parent in a
// `HashMap`, the regions holding `region1` in a `HashSet`, then a walk up
// from `region2` until it meets one of them) on 20 random trees of 10000
// regions built once, each nested broadly or deeply, with 250 random
// pairs asked of each; every region found folded into a checksum.

use std::collections::{HashMap, HashSet};

fn find_smallest_region(regions: &[Vec<String>], region1: &str, region2: &str) -> String {
    let mut parent: HashMap<String, String> = HashMap::new();
    for list in regions {
        for child in &list[1..] {
            parent.insert(child.clone(), list[0].clone());
        }
    }
    let mut holding: HashSet<String> = HashSet::new();
    let mut at = region1.to_string();
    holding.insert(at.clone());
    while let Some(up) = parent.get(&at) {
        at = up.clone();
        holding.insert(at.clone());
    }
    let mut at = region2.to_string();
    while !holding.contains(&at) {
        at = parent[&at].clone();
    }
    at
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn name(i: i64) -> String {
    format!("r{i}")
}

fn random_regions(n: i64, spread: i64, seed: &mut i64) -> Vec<Vec<String>> {
    let mut children: Vec<Vec<i64>> = vec![Vec::new(); n as usize];
    for i in 1..n {
        let lo = (i - spread).max(0);
        let parent = lo + next_random(seed) % (i - lo);
        children[parent as usize].push(i);
    }
    let mut regions = Vec::new();
    for p in 0..n {
        if !children[p as usize].is_empty() {
            let mut list = vec![name(p)];
            list.extend(children[p as usize].iter().map(|&c| name(c)));
            regions.push(list);
        }
    }
    for i in (1..regions.len()).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        regions.swap(i, j);
    }
    regions
}

fn main() {
    let mut seed = 1257;
    let mut trees: Vec<Vec<Vec<String>>> = Vec::new();
    for t in 0..20 {
        let spread = [3, 30, 1000000, 10][t % 4];
        trees.push(random_regions(10000, spread, &mut seed));
    }
    let mut check: i64 = 0;
    for regions in &trees {
        for _ in 0..250 {
            let x = name(next_random(&mut seed) % 10000);
            let y = name(next_random(&mut seed) % 10000);
            let found = find_smallest_region(regions, &x, &y);
            for b in found.bytes() {
                check = (check * 131 + b as i64) % 1000000007;
            }
        }
    }
    println!("20 trees of 10000 regions, 250 pairs each: checksum {check}");
}
