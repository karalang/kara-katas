// Benchmark workload for LeetCode #253 — Meeting Rooms II (Rust mirror).
// Mirrors min_meeting_rooms.kara algorithm-for-algorithm, including the
// hand-rolled binary heap (not BinaryHeap, so both sides run the same sifts).

fn heap_push(heap: &mut Vec<i64>, v: i64) {
    heap.push(v);
    let mut i = heap.len() as i64 - 1;
    while i > 0 {
        let parent = (i - 1) / 2;
        if heap[i as usize] < heap[parent as usize] {
            heap.swap(i as usize, parent as usize);
            i = parent;
        } else {
            break;
        }
    }
}

fn heap_pop(heap: &mut Vec<i64>) {
    let n = heap.len();
    if n == 0 { return; }
    let last = heap.pop().unwrap();
    if n == 1 { return; }
    heap[0] = last;
    let m = heap.len() as i64;
    let mut i: i64 = 0;
    loop {
        let (l, r) = (2 * i + 1, 2 * i + 2);
        let mut smallest = i;
        if l < m && heap[l as usize] < heap[smallest as usize] { smallest = l; }
        if r < m && heap[r as usize] < heap[smallest as usize] { smallest = r; }
        if smallest == i { break; }
        heap.swap(i as usize, smallest as usize);
        i = smallest;
    }
}

fn main() {
    let n: i64 = 150000;
    let rounds: i64 = 25;

    let mut base: Vec<(i64, i64)> = Vec::with_capacity(n as usize);
    let mut state: i64 = 253253;
    for i in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let jitter = (state / 65536) % 8;
        state = (state * 1103515245 + 12345) & 2147483647;
        let dur = (state / 65536) % 60 + 1;
        let s = i + jitter;
        base.push((s, s + dur));
    }
    let mut k = base.len() as i64 - 1;
    while k > 0 {
        state = (state * 1103515245 + 12345) & 2147483647;
        let swap = (state / 65536) % (k + 1);
        base.swap(k as usize, swap as usize);
        k -= 1;
    }

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        let mut s: Vec<(i64, i64)> = base.clone();
        s.sort_by(|a, b| a.0.cmp(&b.0));

        let mut heap: Vec<i64> = Vec::new();
        let mut rooms: i64 = 0;
        for j in 0..n as usize {
            while !heap.is_empty() && heap[0] <= s[j].0 {
                heap_pop(&mut heap);
            }
            heap_push(&mut heap, s[j].1);
            if heap.len() as i64 > rooms { rooms = heap.len() as i64; }
        }
        sink = (sink * 31 + rooms) % 1000000007;
    }
    println!("{}", sink);
}
