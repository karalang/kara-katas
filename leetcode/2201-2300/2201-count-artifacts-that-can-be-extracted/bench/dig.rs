// benchmark's Rust mirror of dig.kara (LeetCode #2201, the ★ arm): the dug
// cells in a `HashSet`, each as r * n + c.
use std::collections::HashSet;

fn dig_artifacts(n: i64, artifacts: &[[i64; 4]], dig: &[[i64; 2]]) -> i64 {
    let mut dug: HashSet<i64> = HashSet::new();
    for d in dig {
        dug.insert(d[0] * n + d[1]);
    }
    let mut count = 0;
    for a in artifacts {
        let mut whole = true;
        for r in a[0]..=a[2] {
            for c in a[1]..=a[3] {
                if !dug.contains(&(r * n + c)) {
                    whole = false;
                }
            }
        }
        if whole {
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn site(n: i64, tries: i64, digs: usize, seed: &mut i64) -> (Vec<[i64; 4]>, Vec<[i64; 2]>) {
    let shapes = [
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (1, 3),
        (3, 1),
        (1, 4),
        (4, 1),
    ];
    let mut taken = vec![false; (n * n) as usize];
    let mut artifacts = Vec::new();
    for _ in 0..tries {
        let (h, w) = shapes[(next_random(seed) % 8) as usize];
        let r = wide_random(seed) % (n - h + 1);
        let c = wide_random(seed) % (n - w + 1);
        let mut free = true;
        for i in r..r + h {
            for j in c..c + w {
                if taken[(i * n + j) as usize] {
                    free = false;
                }
            }
        }
        if free {
            for i in r..r + h {
                for j in c..c + w {
                    taken[(i * n + j) as usize] = true;
                }
            }
            artifacts.push([r, c, r + h - 1, c + w - 1]);
        }
    }
    let mut dug = vec![false; (n * n) as usize];
    let mut dig = Vec::new();
    while dig.len() < digs {
        let cell = wide_random(seed) % (n * n);
        if !dug[cell as usize] {
            dug[cell as usize] = true;
            dig.push([cell / n, cell % n]);
        }
    }
    (artifacts, dig)
}

fn main() {
    let mut seed = 2201;
    let sites: Vec<_> = (0..8)
        .map(|_| site(1000, 20000, 300000, &mut seed))
        .collect();
    let mut check: i64 = 0;
    for _ in 0..10 {
        for (artifacts, dig) in &sites {
            let count = dig_artifacts(1000, artifacts, dig);
            check = (check * 31 + count + artifacts.len() as i64) % 1000000007;
        }
    }
    println!("10 passes over 8 sites: checksum {}", check);
}
