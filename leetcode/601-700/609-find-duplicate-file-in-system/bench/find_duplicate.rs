// Benchmark mirror for #609: the same workload and algorithm as
// find_duplicate.kara (a map from content to paths).
use std::collections::HashMap;

fn find_duplicate(paths: &[String]) -> Vec<Vec<String>> {
    let mut by_content: HashMap<String, Vec<String>> = HashMap::new();
    for line in paths {
        let mut parts = line.split(' ');
        let dir = parts.next().unwrap();
        for file in parts {
            let open = file.find('(').unwrap();
            let name = &file[..open];
            let content = &file[open + 1..file.len() - 1];
            by_content
                .entry(content.to_string())
                .or_default()
                .push(format!("{}/{}", dir, name));
        }
    }
    by_content.into_values().filter(|g| g.len() > 1).collect()
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let systems = 10i64;
    let rounds = 300i64;
    let mut seed: i64 = 609;
    let mut pool: Vec<String> = Vec::new();
    for _ in 0..3000 {
        let mut c = String::new();
        let size = 8 + step(&mut seed) % 13;
        for _ in 0..size {
            c.push((97 + step(&mut seed) % 4) as u8 as char);
        }
        pool.push(c);
    }
    let mut all: Vec<Vec<String>> = Vec::new();
    for s in 0..systems {
        let mut paths = Vec::new();
        let mut counter = 0;
        for d in 0..2000 {
            let mut line = format!("root/s{}/d{}", s, d);
            let files = 1 + step(&mut seed) % 6;
            for _ in 0..files {
                counter += 1;
                let content = &pool[(step(&mut seed) % 3000) as usize];
                line.push_str(&format!(" f{}.txt({})", counter, content));
            }
            paths.push(line);
        }
        all.push(paths);
    }
    let (mut groups, mut files, mut checksum) = (0i64, 0i64, 0i64);
    for r in 0..rounds {
        let found = find_duplicate(&all[((r * 3) % systems) as usize]);
        groups += found.len() as i64;
        for group in &found {
            files += group.len() as i64;
            let length: i64 = group.iter().map(|p| p.len() as i64).sum();
            checksum = (checksum + group.len() as i64 * length) % 1000000007;
        }
    }
    println!("{} systems, {} rounds: {} groups, {} files, checksum {}", systems, rounds, groups, files, checksum);
}
