// LeetCode #2237: Count Positions on Street With Required Brightness --
// the benchmark's Rust mirror of brightness.kara: a difference array, a
// running sum, and the positions meeting their requirement counted.

fn meet_requirement(n: i64, lights: &[[i64; 2]], requirement: &[i64]) -> i64 {
    let mut change = vec![0i64; (n + 1) as usize];
    for light in lights {
        let from = (light[0] - light[1]).max(0);
        let to = (light[0] + light[1]).min(n - 1);
        change[from as usize] += 1;
        change[(to + 1) as usize] -= 1;
    }
    let mut brightness = 0i64;
    let mut count = 0i64;
    for i in 0..n as usize {
        brightness += change[i];
        if brightness >= requirement[i] {
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
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2237i64;
    let n = 100000i64;
    let mut lights: Vec<[i64; 2]> = Vec::new();
    for _ in 0..100000 {
        let position = wide_random(&mut seed) % n;
        let range = wide_random(&mut seed) % 1001;
        lights.push([position, range]);
    }
    let mut requirement: Vec<i64> = Vec::new();
    for _ in 0..n {
        requirement.push(wide_random(&mut seed) % 2001);
    }
    let mut check = 0i64;
    for _ in 0..100 {
        // punch: one light and one requirement drawn again before each pass
        let at = (wide_random(&mut seed) % 100000) as usize;
        let position = wide_random(&mut seed) % n;
        let range = wide_random(&mut seed) % 1001;
        lights[at] = [position, range];
        let place = (wide_random(&mut seed) % n) as usize;
        requirement[place] = wide_random(&mut seed) % 2001;
        check = (check * 31 + meet_requirement(n, &lights, &requirement)) % 1000000007;
    }
    println!("100 passes over 10^5 positions and lights: checksum {}", check);
}
