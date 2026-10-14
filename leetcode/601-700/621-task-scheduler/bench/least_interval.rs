// LeetCode #621: Task Scheduler -- Rust mirror of the Kāra bench.
//
// The ★ arm's frame count over the same lists and rounds; a task is a
// `char`.

fn least_interval(tasks: &[char], n: i64) -> i64 {
    let mut counts = [0i64; 26];
    for &t in tasks {
        counts[(t as i64 - 'A' as i64) as usize] += 1;
    }
    let mut most = 0;
    for &c in counts.iter() {
        if c > most {
            most = c;
        }
    }
    let mut tied = 0;
    for &c in counts.iter() {
        if c == most {
            tied += 1;
        }
    }
    let frame = (most - 1) * (n + 1) + tied;
    frame.max(tasks.len() as i64)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tasks(size: i64, kinds: i64, skew: bool, seed: &mut i64) -> Vec<char> {
    let mut tasks = Vec::new();
    let weight = if skew { kinds * (kinds + 1) / 2 } else { kinds };
    for _ in 0..size {
        let mut r = next_random(seed) % weight;
        let mut k = 0;
        if skew {
            while r > k {
                r -= k + 1;
                k += 1;
            }
        } else {
            k = r;
        }
        tasks.push((65 + k) as u8 as char);
    }
    tasks
}

fn main() {
    let lists = 100;
    let rounds = 30000;
    let mut seed: i64 = 621;
    let mut all: Vec<Vec<char>> = Vec::new();
    for i in 0..lists {
        let kinds = 1 + next_random(&mut seed) % 26;
        all.push(random_tasks(10000, kinds, i % 2 == 0, &mut seed));
    }
    let mut sum: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let answer = least_interval(&all[((r * 7) % lists) as usize], r % 101);
        sum += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{} lists, {} rounds: total {}, checksum {}", lists, rounds, sum, checksum);
}
