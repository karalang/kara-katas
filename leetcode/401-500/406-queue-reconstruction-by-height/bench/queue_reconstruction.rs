// Benchmark for #406: mirror of queue_reconstruction.kara (tallest first,
// each inserted at its k).

fn reconstruct_queue(mut people: Vec<(i64, i64)>) -> Vec<(i64, i64)> {
    people.sort_by_key(|p| (-p.0, p.1));
    let mut queue: Vec<(i64, i64)> = Vec::new();
    for p in people.iter() {
        queue.insert(p.1 as usize, *p);
    }
    queue
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let queues = 1000;
    let n: i64 = 2000;
    let mut seed: i64 = 406;
    let mut rebuilt = 0;
    let mut checksum: i64 = 0;
    for _ in 0..queues {
        let mut count = vec![0i64; 51];
        let mut line: Vec<(i64, i64)> = Vec::new();
        for _ in 0..n {
            let h = 1 + step(&mut seed) % 50;
            let mut k = 0;
            for g in h..51 {
                k += count[g as usize];
            }
            count[h as usize] += 1;
            line.push((h, k));
        }
        let mut people = line.clone();
        for i in (1..n).rev() {
            let j = step(&mut seed) % (i + 1);
            people.swap(i as usize, j as usize);
        }
        let q = reconstruct_queue(people);
        if q == line {
            rebuilt += 1;
        }
        for i in 0..q.len() {
            checksum = (checksum * 31 + q[i].0 * 10000 + q[i].1) % 1000000007;
        }
    }
    println!("{} queues of {} people: {} rebuilt, checksum {}", queues, n, rebuilt, checksum);
}
