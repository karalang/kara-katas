// LeetCode #1233 bench: the ★ arm in Rust, over the same 10 lists of
// 4 · 10^4 folders and 10 passes as the Kāra bench.
use std::collections::HashSet;

fn remove_subfolders(folder: &[String]) -> Vec<String> {
    let mut sorted = folder.to_vec();
    sorted.sort();
    let mut kept: Vec<String> = Vec::new();
    for f in sorted.iter() {
        if kept.is_empty() || !f.starts_with(&format!("{}/", kept[kept.len() - 1])) {
            kept.push(f.clone());
        }
    }
    kept
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters = ["a", "b", "c", "d", "e", "f", "g", "h"];
    let mut seed = 1233;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..10 {
        let mut seen: HashSet<String> = HashSet::new();
        let mut many: Vec<String> = Vec::new();
        while many.len() < 40000 {
            let d = next_random(&mut seed) % 4 + 1;
            let mut f = String::new();
            for level in 0..d {
                f = format!("{}/", f);
                for _ in 0..if level == 0 { 4 } else { 2 } {
                    f = format!("{}{}", f, letters[(next_random(&mut seed) % 8) as usize]);
                }
            }
            if !seen.contains(&f) {
                seen.insert(f.clone());
                many.push(f);
            }
        }
        lists.push(many);
    }
    let mut kept = 0;
    for _ in 0..10 {
        for list in &lists {
            kept += remove_subfolders(list).len();
        }
    }
    println!("10 lists of 40000 folders, 10 passes: {} kept", kept);
}
