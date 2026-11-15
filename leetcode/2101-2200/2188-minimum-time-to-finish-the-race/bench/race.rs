// LeetCode #2188: Minimum Time to Finish the Race -- the benchmark's
// Rust mirror of race.kara, over a slice of the row: the runs on one
// tire, then the laps bottom up.

fn minimum_finish_time(tires: &[[i64; 2]], change_time: i64, num_laps: i64) -> i64 {
    let mut run: Vec<i64> = vec![0];
    for t in tires {
        let (f, r) = (t[0], t[1]);
        let mut lap = f;
        let mut sum = 0;
        let mut k = 1;
        while k <= num_laps && lap <= change_time + f {
            sum += lap;
            if k as usize == run.len() {
                run.push(sum);
            } else if sum < run[k as usize] {
                run[k as usize] = sum;
            }
            lap *= r;
            k += 1;
        }
    }
    let mut best = vec![0i64; (num_laps + 1) as usize];
    for n in 1..=num_laps as usize {
        let mut least = run[1] * n as i64 + change_time * (n as i64 - 1);
        let mut k = 1;
        while k < run.len() && k <= n {
            let pit = if k == n { 0 } else { change_time };
            least = least.min(best[n - k] + pit + run[k]);
            k += 1;
        }
        best[n] = least;
    }
    best[num_laps as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    let b = next_random(seed);
    a * 32768 + b
}

fn main() {
    let mut seed = 2188;
    let mut row: Vec<[i64; 2]> = Vec::with_capacity(100000);
    for _ in 0..100000 {
        let f = big_random(&mut seed) % 100 + 1;
        let r = next_random(&mut seed) % 4 + 2;
        row.push([f, r]);
    }
    let mut check: i64 = 0;
    for _ in 0..5000 {
        let start = (big_random(&mut seed) % 99901) as usize;
        let change_time = big_random(&mut seed) % 100000 + 1;
        let num_laps = 1000;
        let t = minimum_finish_time(&row[start..start + 100], change_time, num_laps);
        check = (check * 31 + t % 1000000007) % 1000000007;
    }
    println!("5000 solves: checksum {}", check);
}
