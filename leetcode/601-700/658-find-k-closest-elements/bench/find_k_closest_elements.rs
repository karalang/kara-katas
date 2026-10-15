// Benchmark for #658: binary search for the window, as the Kara ★ arm.

fn find_closest_elements(arr: &[i64], k: i64, x: i64) -> Vec<i64> {
    let mut low = 0i64;
    let mut high = arr.len() as i64 - k;
    while low < high {
        let middle = (low + high) / 2;
        if x - arr[middle as usize] > arr[(middle + k) as usize] - x {
            low = middle + 1;
        } else {
            high = middle;
        }
    }
    arr[low as usize..(low + k) as usize].to_vec()
}

fn main() {
    let n = 1000000i64;
    let queries = 1000000i64;
    let mut seed: i64 = 658;
    let mut next_random = move || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut arr: Vec<i64> = Vec::with_capacity(n as usize);
    for _ in 0..n {
        let hi = next_random();
        let lo = next_random();
        arr.push((hi * 32768 + lo) % 2000001 - 1000000);
    }
    arr.sort();
    let mut checksum: i64 = 0;
    for q in 0..queries {
        let k = 1 + q % 64;
        let hi = next_random();
        let lo = next_random();
        let x = (hi * 32768 + lo) % 2200001 - 1100000;
        let got = find_closest_elements(&arr, k, x);
        checksum = (checksum * 31 + got[0] * 3 + got[got.len() - 1] * 5 + got.len() as i64 + 10000000) % 1000000007;
    }
    println!("{} numbers, {} queries: checksum {}", n, queries, checksum);
}
