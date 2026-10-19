// Benchmark for #780: Reaching Points -- mirror of the ★ arm (backwards
// by remainders), with the same workload as the Kāra program.

fn reaching_points(sx: i64, sy: i64, tx: i64, ty: i64) -> bool {
    let mut x = tx;
    let mut y = ty;
    while x > sx && y > sy && x != y {
        if x > y {
            x %= y;
        } else {
            y %= x;
        }
    }
    if x == sx && y == sy {
        return true;
    }
    if x == sx && y > sy {
        return (y - sy) % x == 0;
    }
    if y == sy && x > sx {
        return (x - sx) % y == 0;
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1024;
    let mut seed: i64 = 780;
    let mut queries: Vec<(i64, i64, i64, i64)> = Vec::new();
    for q in 0..count {
        let sx = 1 + next_random(&mut seed) % 1000;
        let sy = 1 + next_random(&mut seed) % 1000;
        let mut a = if q % 4 == 3 { sx + 1 } else { sx };
        let mut b = sy;
        while a <= 500000000 && b <= 500000000 {
            if next_random(&mut seed) % 2 == 0 {
                a += b;
            } else {
                b += a;
            }
        }
        if q % 4 == 2 {
            b -= 1;
        }
        queries.push((sx, sy, a, b));
    }
    let mut yes: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..15000i64 {
        for i in 0..count {
            let (sx, sy, tx, ty) = queries[i];
            if reaching_points(sx, sy, tx, ty) {
                yes += 1;
                checksum = (checksum * 31 + i as i64 + round) % 1000000007;
            }
        }
    }
    println!("15000 rounds of 1024 queries: {yes} reachable, checksum {checksum}");
}
