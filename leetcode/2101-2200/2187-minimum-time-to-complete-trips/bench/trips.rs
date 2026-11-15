// LeetCode #2187: Minimum Time to Complete Trips -- the benchmark's Rust
// mirror of trips.kara, over a slice of the row: a binary search over
// the time with the count cut at the total.

fn trips_by(time: &[i64], t: i64, total_trips: i64) -> i64 {
    let mut trips = 0;
    for &x in time {
        trips += t / x;
        if trips >= total_trips {
            break;
        }
    }
    trips
}

fn minimum_time(time: &[i64], total_trips: i64) -> i64 {
    let mut fastest = time[0];
    for &x in time {
        fastest = fastest.min(x);
    }
    let mut lo = 1;
    let mut hi = fastest * total_trips;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if trips_by(time, mid, total_trips) >= total_trips {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
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
    let mut seed = 2187;
    let row: Vec<i64> = (0..1000000).map(|_| big_random(&mut seed) % 10000000 + 1).collect();
    let mut check: i64 = 0;
    for _ in 0..200 {
        let start = (big_random(&mut seed) % 900001) as usize;
        let trips = big_random(&mut seed) % 10000000 + 1;
        let t = minimum_time(&row[start..start + 100000], trips);
        check = (check * 31 + t % 1000000007) % 1000000007;
    }
    println!("200 solves: checksum {}", check);
}
