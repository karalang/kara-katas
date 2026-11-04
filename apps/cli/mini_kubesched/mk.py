"""Writes data/ for mini_kubesched: one cluster of seven nodes in three
zones, the pods of three teams, a file of mistakes, two manifests applied
later (an urgent report and a node joining), and the day's events.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def put(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


put("cluster.nodes", """\
# The production cluster: three zones, a GPU node, a spot node and the
# control plane. Quantities are Kubernetes': cpu in cores or millicores,
# memory with binary (Ki, Mi, Gi) or decimal (k, M, G) suffixes.

node cp-1 cpu=2 memory=4Gi pods=10
  label zone=us-east-1a role=control-plane
  taint node-role=control-plane:NoSchedule

node web-a1 cpu=4 memory=16Gi pods=12
  label zone=us-east-1a disktype=ssd pool=general generation=5

node web-b1 cpu=4 memory=16Gi pods=12
  label zone=us-east-1b disktype=ssd pool=general generation=6

node web-c1 cpu=3500m memory=8Gi pods=12
  label zone=us-east-1c disktype=hdd pool=general generation=4

node big-b2 cpu=16 memory=64Gi pods=30
  label zone=us-east-1b disktype=ssd pool=general generation=6
  taint maintenance=soon:PreferNoSchedule

node gpu-a2 cpu=8 memory=32Gi pods=8
  label zone=us-east-1a pool=gpu accelerator=nvidia-a100
  taint nvidia.com/gpu=present:NoSchedule

node spot-c2 cpu=8 memory=16000M pods=20
  label zone=us-east-1c pool=spot
  taint spot=true:PreferNoSchedule
""")

put("system.pods", """\
# kube-system: DNS twice, never two on one node; the metrics server; an
# ingress controller in each zone; a log shipper that tolerates anything.

pod kube-system/coredns-1 priority=2000
  request cpu=100m memory=70Mi
  label app=coredns
  apart hostname app=coredns
  tolerate node-role=control-plane:NoSchedule

pod kube-system/coredns-2 priority=2000
  request cpu=100m memory=70Mi
  label app=coredns
  apart hostname app=coredns
  tolerate node-role=control-plane:NoSchedule

pod kube-system/metrics-server priority=2000
  request cpu=100m memory=200Mi
  label app=metrics-server
  require pool In general

pod kube-system/ingress-1 priority=1500
  request cpu=500m memory=512Mi
  label app=ingress
  spread zone 1 app=ingress
  require pool In general,spot

pod kube-system/ingress-2 priority=1500
  request cpu=500m memory=512Mi
  label app=ingress
  spread zone 1 app=ingress
  require pool In general,spot

pod kube-system/ingress-3 priority=1500
  request cpu=500m memory=512Mi
  label app=ingress
  spread zone 1 app=ingress
  require pool In general,spot

pod kube-system/fluent-bit priority=1800
  request cpu=50m memory=64Mi
  label app=fluent-bit
  tolerate *
  select role=control-plane
""")

web = ["""\
# The shop: a storefront spread over the zones, an API that keeps one
# replica per node, a cache that wants SSDs and newer machines.
"""]
for i in range(1, 7):
    web.append(f"""
pod shop/storefront-{i} priority=1000
  request cpu=300m memory=384Mi
  label app=storefront tier=web
  spread zone 1 app=storefront
""")
for i in range(1, 5):
    web.append(f"""
pod shop/api-{i} priority=1000
  request cpu=600m memory=1Gi
  label app=api tier=backend
  apart hostname app=api
  prefer 50 generation Gt 5
""")
web.append("""
pod shop/redis-0 priority=1200
  request cpu=1 memory=6Gi
  label app=redis tier=cache
  select disktype=ssd
  prefer 80 generation Gt 5
  prefer 20 zone In us-east-1b

pod shop/redis-1 priority=1200
  request cpu=1 memory=6Gi
  label app=redis tier=cache
  select disktype=ssd
  apart zone app=redis
  prefer 80 generation Gt 5

pod shop/search priority=900
  label app=search
  prefer 10 pool In spot
""")
put("web.pods", "".join(web))

batch = ["""\
# Data team: nightly jobs at priority 0 that soak up the big node, best
# effort jobs below that, and a training run that needs the GPU.
"""]
for i in range(1, 6):
    batch.append(f"""
pod data/etl-{i}
  request cpu=2500m memory=10Gi
  label app=etl
  require pool In general
  require generation Gt 5
  tolerate maintenance:PreferNoSchedule
""")
for i in range(1, 4):
    batch.append(f"""
pod data/scratch-{i} priority=-10
  request cpu=1 memory=2Gi
  label app=scratch
""")
batch.append("""
pod data/train-llm priority=100
  request cpu=6 memory=24Gi
  label app=train
  select accelerator=nvidia-a100
  tolerate nvidia.com/gpu=present:NoSchedule

pod data/train-small priority=100
  request cpu=4 memory=12Gi
  label app=train
  select accelerator=nvidia-a100
""")
put("batch.pods", "".join(batch))

put("zz_broken.pods", """\
# Mistakes a manifest review would catch.
pod nightly-backup priority=10
  request cpu=1
  sidecar logrotate
pod data/backup priority=high
pod data/report
  request cpu=1.25 memory=3Gb
pod data/report-2
  request cpu=250m
  tolerate dedicated=batch:Sometimes
pod data/report-3
  require zone Near us-east-1a
pod data/report-4
  spread zone 0 app=report
node web-a1 cpu=4 memory=16Gi pods=12
node tiny cpu=1
  label zone=us-east-1a
  request cpu=1
deployment shop/frontend
pod shop/storefront-3 priority=1000
  request cpu=300m memory=384Mi
""")

put("urgent.later", """\
# Applied mid-day: a quarter-end report that must run now, on general
# nodes in us-east-1b.
pod finance/quarter-close priority=500
  request cpu=12 memory=40Gi
  label app=quarter-close
  require zone In us-east-1b
  require pool In general
""")

put("scaleup.later", """\
# The autoscaler adds a node in us-east-1c, and the shop scales out.
node web-c3 cpu=8 memory=32Gi pods=16
  label zone=us-east-1c disktype=ssd pool=general generation=7

pod shop/storefront-7 priority=1000
  request cpu=300m memory=384Mi
  label app=storefront tier=web
  spread zone 1 app=storefront

pod shop/api-5 priority=1000
  request cpu=600m memory=1Gi
  label app=api tier=backend
  apart hostname app=api
  prefer 50 generation Gt 5
""")

put("events.txt", """\
# One day on the cluster.
schedule
show nodes
show pods
show pending

# The urgent report preempts batch work on the big node.
apply data/urgent.later
schedule
show pending

# Patch web-b1: drain it, reschedule, bring it back.
drain web-b1
schedule
uncordon web-b1
schedule

# Spot capacity is reclaimed.
taint spot-c2 spot=reclaim:NoExecute
schedule

# A zone c node dies; the autoscaler replaces it.
fail web-c1
schedule
apply data/scaleup.later
schedule

# The training runs finish; the GPU taint goes away for maintenance.
delete data/train-llm
untaint gpu-a2 nvidia.com/gpu
schedule
delete shop/nope
cordon nowhere
reboot web-a1
apply data/missing.later
show nodes
show pods
show pending
""")
