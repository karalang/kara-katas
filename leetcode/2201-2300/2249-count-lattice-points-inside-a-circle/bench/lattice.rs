// LeetCode #2249: Count Lattice Points Inside a Circle -- the benchmark's
// Rust mirror of lattice.kara: every point of the box bounding the
// circles tried against them until one holds it.

fn count_lattice_points(circles: &[[i64; 3]]) -> i64 {
    let left = circles.iter().map(|c| c[0] - c[2]).min().unwrap();
    let right = circles.iter().map(|c| c[0] + c[2]).max().unwrap();
    let bottom = circles.iter().map(|c| c[1] - c[2]).min().unwrap();
    let top = circles.iter().map(|c| c[1] + c[2]).max().unwrap();
    let mut count = 0;
    for px in left..right + 1 {
        for py in bottom..top + 1 {
            for c in circles {
                let dx = px - c[0];
                let dy = py - c[1];
                if dx * dx + dy * dy <= c[2] * c[2] {
                    count += 1;
                    break;
                }
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2249i64;
    let mut check = 0i64;
    for _ in 0..100 {
        let circles: Vec<[i64; 3]> = (0..200)
            .map(|_| {
                let x = next_random(&mut seed) % 100 + 1;
                let y = next_random(&mut seed) % 100 + 1;
                let r = next_random(&mut seed) % x.min(y) + 1;
                [x, y, r]
            })
            .collect();
        check = (check * 31 + count_lattice_points(&circles)) % 1000000007;
    }
    println!("100 cases of 200 circles: checksum {}", check);
}
