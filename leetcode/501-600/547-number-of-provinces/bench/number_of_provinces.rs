// Benchmark for #547: Rust mirror of the ★ arm (depth-first search); see
// number_of_provinces.kara.

fn visit(is_connected: &[Vec<i64>], city: usize, seen: &mut Vec<bool>) {
    seen[city] = true;
    for other in 0..is_connected.len() {
        if is_connected[city][other] == 1 && !seen[other] {
            visit(is_connected, other, seen);
        }
    }
}

fn find_circle_num(is_connected: &[Vec<i64>]) -> i64 {
    let n = is_connected.len();
    let mut seen = vec![false; n];
    let mut provinces = 0;
    for city in 0..n {
        if !seen[city] {
            provinces += 1;
            visit(is_connected, city, &mut seen);
        }
    }
    provinces
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 30;
    let n = 200;
    let mut seed: i64 = 547;
    let mut all: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..count {
        let mut m: Vec<Vec<i64>> = Vec::new();
        for i in 0..n {
            let mut row = vec![0; n];
            row[i] = 1;
            m.push(row);
        }
        for i in 0..n {
            for j in i + 1..n {
                if next_random(&mut seed) % 1000 < 1 + (g % 10) as i64 {
                    m[i][j] = 1;
                    m[j][i] = 1;
                }
            }
        }
        all.push(m);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..200 {
        for g in 0..count {
            let a = (round * 13 + g) % n;
            let b = (round * 29 + g * 3 + 1) % n;
            if a != b {
                let flip = 1 - all[g][a][b];
                all[g][a][b] = flip;
                all[g][b][a] = flip;
            }
            let p = find_circle_num(&all[g]);
            total += p;
            checksum = (checksum * 31 + p) % 1000000007;
        }
    }
    println!("{} matrices, 200 rounds each: {} provinces, checksum {}", count, total, checksum);
}
