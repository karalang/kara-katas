struct Queue {
    data: Vec<i64>,
    head: i64,
}

fn q_new() -> Queue {
    Queue { data: Vec::new(), head: 0 }
}

fn q_size(q: &Queue) -> i64 {
    q.data.len() as i64 - q.head
}

fn q_enqueue(q: &mut Queue, x: i64) {
    q.data.push(x);
}

fn q_dequeue(q: &mut Queue) -> i64 {
    let v = q.data[q.head as usize];
    q.head += 1;
    v
}

fn q_front(q: &Queue) -> i64 {
    q.data[q.head as usize]
}

fn stack_push(q: &mut Queue, x: i64) {
    q_enqueue(q, x);
    let mut rotations = q_size(q) - 1;
    while rotations > 0 {
        let front = q_dequeue(q);
        q_enqueue(q, front);
        rotations -= 1;
    }
}

fn stack_pop(q: &mut Queue) -> i64 {
    q_dequeue(q)
}

fn stack_top(q: &Queue) -> i64 {
    q_front(q)
}

fn main() {
    let passes: i64 = 12000;
    let ops_per_pass: i64 = 1500;
    let cap: i64 = 48;
    let modulus: i64 = 1000000007;

    let mut state: i64 = 12345;
    let mut sink: i64 = 0;
    for _ in 0..passes {
        let mut s = q_new();
        for _ in 0..ops_per_pass {
            state = (state * 1103515245 + 12345) & 2147483647;
            let v = (state % 1000) + 1;
            let sel = state % 4;
            let size = q_size(&s);
            if size == 0 {
                stack_push(&mut s, v);
            } else if size >= cap {
                if state & 1 == 0 {
                    sink = (sink + stack_pop(&mut s)) % modulus;
                } else {
                    sink = (sink + stack_top(&s)) % modulus;
                }
            } else if sel <= 1 {
                stack_push(&mut s, v);
            } else if sel == 2 {
                sink = (sink + stack_pop(&mut s)) % modulus;
            } else {
                sink = (sink + stack_top(&s)) % modulus;
            }
        }
    }
    println!("{}", sink);
}
