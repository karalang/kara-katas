// LeetCode #2021: Brightest Position on Street -- the ★ arm's benchmark, a
// mirror of brightest.kara: the events built and sorted per call.

fn brightest_position(lights: &[(i64, i64)]) -> i64 {
    let mut events: Vec<(i64, i64)> = Vec::new();
    for &(position, range) in lights.iter() {
        events.push((position - range, 1));
        events.push((position + range + 1, -1));
    }
    events.sort();
    let (mut brightness, mut best, mut answer) = (0i64, 0i64, 0i64);
    let mut i = 0;
    while i < events.len() {
        let at = events[i].0;
        while i < events.len() && events[i].0 == at {
            brightness += events[i].1;
            i += 1;
        }
        if brightness > best {
            best = brightness;
            answer = at;
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2021;
    let mut streets: Vec<Vec<(i64, i64)>> = Vec::new();
    for s in 0..100usize {
        let spread = [1000000i64, 10000000, 100000000][s % 3];
        let reach = [1000i64, 100000, 1000000][s % 3];
        let mut lights = Vec::new();
        for _ in 0..10000 {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            let position = (hi * 32768 + lo) % (2 * spread + 1) - spread;
            lights.push((position, next_random(&mut seed) % (reach + 1)));
        }
        streets.push(lights);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..5 {
        for lights in streets.iter() {
            let answer = brightest_position(lights);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer + 1000000000) % 1000000007;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
