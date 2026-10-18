// LeetCode #703 bench: the heap arm in Rust. See the .kara twin for the
// workload.

struct KthLargest {
    k: usize,
    heap: Vec<i64>,
}

impl KthLargest {
    fn new(k: usize, nums: Vec<i64>) -> KthLargest {
        let mut s = KthLargest { k, heap: Vec::new() };
        for &x in nums.iter() {
            s.add(x);
        }
        s
    }

    fn add(&mut self, val: i64) -> i64 {
        if self.heap.len() < self.k {
            self.heap.push(val);
            let mut i = self.heap.len() - 1;
            while i > 0 {
                let parent = (i - 1) / 2;
                if self.heap[parent] <= self.heap[i] {
                    break;
                }
                self.heap.swap(parent, i);
                i = parent;
            }
        } else if val > self.heap[0] {
            self.heap[0] = val;
            let n = self.heap.len();
            let mut i = 0;
            loop {
                let left = 2 * i + 1;
                let right = left + 1;
                let mut least = i;
                if left < n && self.heap[left] < self.heap[least] {
                    least = left;
                }
                if right < n && self.heap[right] < self.heap[least] {
                    least = right;
                }
                if least == i {
                    break;
                }
                self.heap.swap(least, i);
                i = least;
            }
        }
        self.heap[0]
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 703;
    let mut checksum: i64 = 0;
    let mut changes: i64 = 0;
    for _ in 0..5 {
        for stream in 0..10 {
            let k = 50 * (stream + 1);
            let mut price: i64 = 100000;
            let mut nums: Vec<i64> = Vec::new();
            for _ in 0..1000 {
                price += next_random(&mut seed) % 201 - 90;
                nums.push(price);
            }
            let mut s = KthLargest::new(k, nums);
            let mut last = 0;
            for _ in 0..200000 {
                price += next_random(&mut seed) % 201 - 90;
                let answer = s.add(price);
                if answer != last {
                    changes += 1;
                }
                last = answer;
                checksum = (checksum * 31 + answer) % 1000000007;
            }
        }
    }
    println!("5 rounds of 10 streams of 200000 prices: answer changed {changes} times, checksum {checksum}");
}
