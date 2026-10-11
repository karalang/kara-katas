// Benchmark for #370 -- mirror of range_addition.kara.

fn get_modified_array(length: usize, updates: &[(usize, usize, i64)]) -> Vec<i64> {
    let mut diff = vec![0i64; length + 1];
    for &(start, end, inc) in updates {
        diff[start] += inc;
        diff[end + 1] -= inc;
    }
    let mut out = vec![0i64; length];
    let mut running = 0;
    for i in 0..length {
        running += diff[i];
        out[i] = running;
    }
    out
}

fn main() {
    let mut seed: i64 = 370;
    let mut checksum: i64 = 0;
    for _ in 0..50 {
        let mut updates = Vec::with_capacity(10000);
        for _ in 0..10000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let high = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let a = (high * 32768 + seed / 65536) % 100000;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let high2 = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let b = (high2 * 32768 + seed / 65536) % 100000;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let inc = (seed / 65536) % 2001 - 1000;
            updates.push((a.min(b) as usize, a.max(b) as usize, inc));
        }
        let out = get_modified_array(100000, &updates);
        for v in &out {
            checksum = (checksum * 31 + v + 100000000) % 1000000007;
        }
    }
    println!("checksum {}", checksum);
}
