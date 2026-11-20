// LeetCode #1238: the benchmark, mirroring the Kāra file.

fn circular_permutation(n: i64, start: i64) -> Vec<i64> {
    (0..1i64 << n).map(|i| start ^ i ^ (i >> 1)).collect()
}

fn is_cycle(n: i64, start: i64, p: &[i64]) -> bool {
    let size = 1i64 << n;
    if p.len() as i64 != size || p[0] != start {
        return false;
    }
    let mut seen = vec![false; size as usize];
    for &v in p {
        if v < 0 || v >= size || seen[v as usize] {
            return false;
        }
        seen[v as usize] = true;
    }
    for i in 0..size as usize {
        let d = p[i] ^ p[(i + 1) % size as usize];
        if d == 0 || d & (d - 1) != 0 {
            return false;
        }
    }
    true
}

fn main() {
    let mut cycles = 0;
    let mut check: i64 = 0;
    for k in 0..64i64 {
        let start = (k * 1031) % 65536;
        let p = circular_permutation(16, start);
        if is_cycle(16, start, &p) {
            cycles += 1;
        }
        check = (check * 131 + p[32768]) % 1000000007;
    }
    println!("n = 16, 64 starts: {} cycles, checksum {}", cycles, check);
}
