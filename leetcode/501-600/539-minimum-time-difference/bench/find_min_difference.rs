// Benchmark for #539: Rust mirror of the ★ arm (minutes, sorted); see
// find_min_difference.kara.

fn minutes(t: &str) -> i64 {
    t[0..2].parse::<i64>().unwrap() * 60 + t[3..5].parse::<i64>().unwrap()
}

fn find_min_difference(time_points: &[String]) -> i64 {
    let mut mins: Vec<i64> = time_points.iter().map(|t| minutes(t)).collect();
    mins.sort();
    let mut best = mins[0] + 1440 - mins[mins.len() - 1];
    for i in 1..mins.len() {
        best = best.min(mins[i] - mins[i - 1]);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn clock(minute: i64) -> String {
    format!("{:02}:{:02}", minute / 60, minute % 60)
}

fn main() {
    // 300 lists of 20 to 1,440 distinct times, the first places of a
    // shuffle of the whole day, built once. Then the answer for each
    // list is found 100 times.
    let lists = 300;
    let mut seed: i64 = 539;
    let mut day: Vec<i64> = (0..1440).collect();
    let mut all: Vec<Vec<String>> = Vec::new();
    let mut total_times = 0;
    for _ in 0..lists {
        let size = 20 + next_random(&mut seed) % 1421;
        let mut times = Vec::new();
        for i in 0..size {
            let j = i + next_random(&mut seed) % (1440 - i);
            day.swap(i as usize, j as usize);
            times.push(clock(day[i as usize]));
        }
        total_times += size;
        all.push(times);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..100 {
        for times in &all {
            let answer = find_min_difference(times);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    println!("{lists} lists, {total_times} times, 100 times each: total {total}, checksum {checksum}");
}
