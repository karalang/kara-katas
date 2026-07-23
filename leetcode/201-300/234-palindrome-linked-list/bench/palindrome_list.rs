struct Node {
    val: i64,
    next: i64,
}

fn reverse(nodes: &mut [Node], head: i64) -> i64 {
    let mut prev = -1i64;
    let mut cur = head;
    while cur != -1 {
        let nxt = nodes[cur as usize].next;
        nodes[cur as usize].next = prev;
        prev = cur;
        cur = nxt;
    }
    prev
}

fn is_palindrome(nodes: &mut [Node], head: i64) -> bool {
    if head == -1 {
        return true;
    }

    let mut slow = head;
    let mut fast = head;
    while nodes[fast as usize].next != -1
        && nodes[nodes[fast as usize].next as usize].next != -1
    {
        slow = nodes[slow as usize].next;
        fast = nodes[nodes[fast as usize].next as usize].next;
    }

    let start = nodes[slow as usize].next;
    let second = reverse(nodes, start);
    let mut p1 = head;
    let mut p2 = second;
    while p2 != -1 {
        if nodes[p1 as usize].val != nodes[p2 as usize].val {
            return false;
        }
        p1 = nodes[p1 as usize].next;
        p2 = nodes[p2 as usize].next;
    }
    true
}

fn main() {
    let l: i64 = 50000;
    let passes: i64 = 1800;
    let half = (l + 1) / 2;

    let mut fh: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..half {
        state = (state * 1103515245 + 12345) & 2147483647;
        fh.push(state % 1000);
    }

    let mut nodes: Vec<Node> = Vec::new();
    for j in 0..l {
        let v = if j < half {
            fh[j as usize]
        } else {
            fh[(l - 1 - j) as usize]
        };
        let next = if j + 1 < l { j + 1 } else { -1 };
        nodes.push(Node { val: v, next });
    }

    let head: i64 = 0;
    let mid = l / 2 - 1;
    let base_mid = nodes[mid as usize].val;

    let mut sink: i64 = 0;
    for p in 0..passes {
        for k in 0..l {
            nodes[k as usize].next = if k + 1 < l { k + 1 } else { -1 };
        }
        nodes[mid as usize].val = base_mid + (p % 2);
        if is_palindrome(&mut nodes, head) {
            sink += 1;
        }
    }
    println!("{}", sink);
}
