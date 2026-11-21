// LeetCode #1574: Shortest Subarray to be Removed to Make Array Sorted --
// bench: the ★ arm (a sorted prefix joined to a sorted suffix by two
// pointers) over 20 arrays of 500000 values, each a rising first half, a
// stretch of random values and a rising second half that starts low, built
// once; then 3 rounds answering all 20, 60 answers.

fn shortest(arr: &[i64]) -> i64 {
    let n = arr.len();
    let mut left = 0;
    while left + 1 < n && arr[left] <= arr[left + 1] {
        left += 1;
    }
    if left == n - 1 {
        return 0;
    }
    let mut right = n - 1;
    while right > 0 && arr[right - 1] <= arr[right] {
        right -= 1;
    }
    let mut best = (n - left - 1).min(right);
    let mut j = right;
    for i in 0..left + 1 {
        while j < n && arr[j] < arr[i] {
            j += 1;
        }
        best = best.min(j - i - 1);
    }
    best as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n: i64 = 500000;
    let mut seed = 1574;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let middle = next_random(&mut seed) % 1000 + 1;
        let start = (n - middle) / 2;
        let mut arr: Vec<i64> = Vec::new();
        let mut v = 0;
        for i in 0..n {
            if i == start + middle {
                v = next_random(&mut seed) % 1000;
            }
            if i >= start && i < start + middle {
                arr.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 4000000);
            } else {
                v += next_random(&mut seed) % 8;
                arr.push(v);
            }
        }
        arrays.push(arr);
    }
    let (mut check, mut total) = (0i64, 0i64);
    for _ in 0..3 {
        for arr in &arrays {
            let length = shortest(arr);
            total += length;
            check = mix(check, length);
        }
    }
    println!("60 answers over 20 arrays of {} values: lengths total {}, checksum {}", n, total, check);
}
