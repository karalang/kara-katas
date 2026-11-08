// LeetCode #2015: Average Height of Buildings in Each Segment -- the ★ arm's
// benchmark, a mirror of average.kara.

fn average_height_of_buildings(buildings: &[(i64, i64, i64)]) -> Vec<(i64, i64, i64)> {
    let mut events: Vec<(i64, i64, i64)> = Vec::new();
    for &(start, end, height) in buildings {
        events.push((start, height, 1));
        events.push((end, -height, -1));
    }
    events.sort();
    let mut street: Vec<(i64, i64, i64)> = Vec::new();
    let (mut sum, mut count, mut i) = (0i64, 0i64, 0usize);
    while i < events.len() {
        let at = events[i].0;
        while i < events.len() && events[i].0 == at {
            sum += events[i].1;
            count += events[i].2;
            i += 1;
        }
        if count == 0 {
            continue;
        }
        let next = events[i].0;
        let average = sum / count;
        let n = street.len();
        if n > 0 && street[n - 1].1 == at && street[n - 1].2 == average {
            street[n - 1].1 = next;
        } else {
            street.push((at, next, average));
        }
    }
    street
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2015i64;
    let mut streets: Vec<Vec<(i64, i64, i64)>> = Vec::new();
    for s in 0..60i64 {
        let mut buildings = Vec::new();
        for _ in 0..10000 {
            let start = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000;
            let end = start + next_random(&mut seed) % (100 * (s + 1)) + 1;
            buildings.push((start, end, next_random(&mut seed) % (s + 2) + 1));
        }
        streets.push(buildings);
    }
    let (mut calls, mut segments, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..5 {
        for buildings in &streets {
            let street = average_height_of_buildings(buildings);
            calls += 1;
            segments += street.len() as i64;
            for &(left, right, average) in &street {
                check = (check * 31 + left + right * 7 + average * 13) % 1000000007;
            }
        }
    }
    println!("{calls} calls: {segments} segments, checksum {check}");
}
