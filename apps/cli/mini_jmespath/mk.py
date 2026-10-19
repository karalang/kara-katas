# Writes data/ for mini_jmespath: the JMESPath compliance suite (copied from
# suite/), command-line output of the kind people query with `--query` or
# `jp` (EC2 instances, an S3 listing, CloudWatch datapoints, IAM policies,
# kubectl pods, GitHub issues), the jobs that query them, and a set of
# random expressions, some of them broken on purpose, for the parser.
import json
import os
import random
import shutil

D = "data"


def w(path, text):
    p = os.path.join(D, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def wj(path, value, indent=4):
    w(path, json.dumps(value, indent=indent, ensure_ascii=False) + "\n")


if os.path.isdir(D):
    shutil.rmtree(D)
SUITE = sorted(f for f in os.listdir("suite") if f.endswith(".json"))
os.makedirs(os.path.join(D, "suite"))
for f in SUITE:
    shutil.copy(os.path.join("suite", f), os.path.join(D, "suite", f))

rnd = random.Random(20261019)


def stamp(day, sec):
    h, m, s = sec // 3600, sec // 60 % 60, sec % 60
    return "2026-%02d-%02dT%02d:%02d:%02d.000Z" % (9 + day // 30, day % 30 + 1, h, m, s)


# ---------------------------------------------------------------- EC2
TYPES = ["t3.micro", "t3.medium", "m6i.large", "m6i.xlarge", "c7g.2xlarge", "r6g.large"]
STATES = [(16, "running")] * 6 + [(80, "stopped")] * 2 + [(0, "pending"), (48, "terminated")]
TEAMS = ["payments", "search", "platform", "data"]
reservations = []
n = 0
for r in range(5):
    inst = []
    for k in range(rnd.randint(2, 6)):
        n += 1
        code, name = rnd.choice(STATES)
        az = "eu-west-1" + rnd.choice("abc")
        it = {
            "AmiLaunchIndex": k,
            "ImageId": "ami-0%015x" % rnd.getrandbits(60),
            "InstanceId": "i-0%016x" % rnd.getrandbits(64),
            "InstanceType": rnd.choice(TYPES),
            "LaunchTime": stamp(rnd.randint(0, 40), rnd.randint(0, 86399)),
            "Monitoring": {"State": rnd.choice(["disabled", "enabled"])},
            "Placement": {"AvailabilityZone": az, "Tenancy": "default"},
            "PrivateIpAddress": "10.%d.%d.%d" % (r, rnd.randint(0, 255), rnd.randint(1, 254)),
            "State": {"Code": code, "Name": name},
            "SubnetId": "subnet-0%016x" % rnd.getrandbits(64),
            "VpcId": "vpc-0a1b2c3d4e5f60718",
            "Architecture": "x86_64",
            "CpuOptions": {"CoreCount": rnd.choice([1, 2, 4]), "ThreadsPerCore": rnd.choice([1, 2])},
            "BlockDeviceMappings": [
                {"DeviceName": "/dev/xvd" + "abcdef"[d],
                 "Ebs": {"VolumeId": "vol-0%016x" % rnd.getrandbits(64),
                         "Status": "attached", "DeleteOnTermination": d == 0}}
                for d in range(rnd.randint(1, 3))
            ],
            "SecurityGroups": [
                {"GroupName": g, "GroupId": "sg-0%016x" % (7919 * len(g) + 4099)}
                for g in (rnd.sample(["web", "ssh-admin", "db-clients", "monitoring"], rnd.randint(1, 3)))
            ],
        }
        if "g." in it["InstanceType"]:
            it["Architecture"] = "arm64"
        if name == "running" and rnd.random() < 0.5:
            it["PublicIpAddress"] = "203.0.113.%d" % rnd.randint(1, 254)
            it["PublicDnsName"] = "ec2-203-0-113-%s.eu-west-1.compute.amazonaws.com" % it["PublicIpAddress"].split(".")[-1]
        else:
            it["PublicDnsName"] = ""
        tags = []
        if rnd.random() < 0.9:
            tags.append({"Key": "Name", "Value": "%s-%s-%02d" % (rnd.choice(TEAMS), rnd.choice(["api", "worker", "cron"]), n)})
        tags.append({"Key": "env", "Value": rnd.choice(["prod", "prod", "staging", "dev"])})
        if rnd.random() < 0.7:
            tags.append({"Key": "team", "Value": rnd.choice(TEAMS)})
        if rnd.random() < 0.3:
            tags.append({"Key": "aws:autoscaling:groupName", "Value": "asg-%d" % r})
        rnd.shuffle(tags)
        if rnd.random() < 0.92:
            it["Tags"] = tags
        inst.append(it)
    reservations.append({"Groups": [], "Instances": inst, "OwnerId": "123456789012",
                         "ReservationId": "r-0%016x" % rnd.getrandbits(64)})
wj("aws/ec2-describe-instances.json", {"Reservations": reservations})

# ---------------------------------------------------------------- S3
objs = []
for i in range(60):
    kind = rnd.choice(["logs", "logs", "images", "backups", "exports"])
    if kind == "logs":
        key = "logs/2026/%02d/%02d/app-%02d.log.gz" % (rnd.randint(9, 10), rnd.randint(1, 28), rnd.randint(1, 4))
        size = rnd.randint(2000, 900000)
    elif kind == "images":
        key = "images/%s/%s.%s" % (rnd.choice(["avatars", "products"]), "%06d" % rnd.randint(0, 999999), rnd.choice(["png", "jpg", "webp"]))
        size = rnd.randint(8000, 4000000)
    elif kind == "backups":
        key = "backups/db-2026-%02d-%02d.sql.gz" % (rnd.randint(9, 10), rnd.randint(1, 28))
        size = rnd.randint(500000000, 9000000000)
    else:
        key = "exports/report %d (%s).csv" % (i, rnd.choice(["final", "draft", "über"]))
        size = rnd.randint(0, 50000)
    objs.append({"Key": key, "LastModified": stamp(rnd.randint(0, 40), rnd.randint(0, 86399)).replace(".000Z", "+00:00"),
                 "ETag": "\"%032x\"" % rnd.getrandbits(128), "Size": size,
                 "StorageClass": rnd.choice(["STANDARD", "STANDARD", "STANDARD_IA", "GLACIER"])})
uniq = {}
for o in objs:
    uniq[o["Key"]] = o
objs = sorted(uniq.values(), key=lambda o: o["Key"])
wj("aws/s3-list-objects-v2.json", {"IsTruncated": False, "Contents": objs, "Name": "acme-shop-assets",
                                   "Prefix": "", "MaxKeys": 1000, "EncodingType": "url", "KeyCount": len(objs)})

# ---------------------------------------------------------------- CloudWatch
pts = []
for i in range(36):
    avg = round(rnd.uniform(5, 95), rnd.choice([1, 2, 6, 12]))
    pts.append({"Timestamp": "2026-10-18T%02d:%02d:00+00:00" % (i // 4, i % 4 * 15),
                "SampleCount": 15.0, "Average": avg, "Maximum": round(avg + rnd.uniform(0, 4.9), 3),
                "Minimum": round(max(0.0, avg - rnd.uniform(0, 5)), 3), "Unit": "Percent"})
rnd.shuffle(pts)
wj("aws/cloudwatch-cpu.json", {"Label": "CPUUtilization", "Datapoints": pts})

# ---------------------------------------------------------------- IAM
policies = []
for name in ["ReadOnlyBilling", "S3AssetsWriter", "CiDeployRole-Policy", "PaymentsDbAccess", "LegacyFullAccess", "SupportTicketsRead"]:
    policies.append({"PolicyName": name, "PolicyId": "ANPA%016X" % rnd.getrandbits(64),
                     "Arn": "arn:aws:iam::123456789012:policy/" + name, "Path": "/",
                     "DefaultVersionId": "v%d" % rnd.randint(1, 6), "AttachmentCount": rnd.choice([0, 0, 1, 2, 5]),
                     "PermissionsBoundaryUsageCount": 0, "IsAttachable": True,
                     "CreateDate": stamp(rnd.randint(0, 40), 3600).replace(".000Z", "+00:00")})
wj("aws/iam-list-policies.json", {"Policies": policies, "IsTruncated": False})
doc = {"Version": "2012-10-17", "Statement": [
    {"Sid": "ReadAssets", "Effect": "Allow", "Action": ["s3:GetObject", "s3:ListBucket"],
     "Resource": ["arn:aws:s3:::acme-shop-assets", "arn:aws:s3:::acme-shop-assets/*"]},
    {"Sid": "WriteExports", "Effect": "Allow", "Action": "s3:PutObject",
     "Resource": "arn:aws:s3:::acme-shop-assets/exports/*",
     "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}},
    {"Effect": "Deny", "Action": ["s3:DeleteObject", "s3:DeleteBucket"], "Resource": "*",
     "Condition": {"Bool": {"aws:MultiFactorAuthPresent": "false"}}},
    {"Sid": "Kms", "Effect": "Allow", "Action": ["kms:Decrypt", "kms:GenerateDataKey*"],
     "Resource": "arn:aws:kms:eu-west-1:123456789012:key/0f1e2d3c-4b5a-6978-8a9b-0c1d2e3f4a5b"},
]}
wj("aws/iam-policy-document.json", {"PolicyVersion": {"Document": doc, "VersionId": "v3", "IsDefaultVersion": True}})

# ---------------------------------------------------------------- kubectl
pods = []
apps = [("checkout", "shop", 3), ("cart", "shop", 2), ("search-indexer", "search", 2),
        ("prometheus", "monitoring", 1), ("coredns", "kube-system", 2), ("payments-db", "shop", 1)]
nodes = ["ip-10-0-1-17.eu-west-1.compute.internal", "ip-10-0-2-41.eu-west-1.compute.internal",
         "ip-10-0-3-9.eu-west-1.compute.internal"]
for app, ns, reps in apps:
    for r in range(reps):
        suffix = "%08x" % rnd.getrandbits(32)
        name = "%s-%s-%s" % (app, suffix[:5], suffix[5:] + "xz"[r % 2])
        conts = [{"name": app, "image": "registry.example.com/%s:1.%d.%d" % (app, rnd.randint(0, 9), rnd.randint(0, 20)),
                  "ports": [{"containerPort": rnd.choice([8080, 9090, 53, 5432]), "protocol": "TCP"}],
                  "resources": {"requests": {"cpu": rnd.choice(["100m", "250m", "500m", "1"]), "memory": rnd.choice(["128Mi", "512Mi", "1Gi"])},
                                "limits": {"memory": rnd.choice(["256Mi", "1Gi", "2Gi"])}}}]
        if app in ("checkout", "cart"):
            conts.append({"name": "envoy", "image": "envoyproxy/envoy:v1.31.2",
                          "ports": [{"containerPort": 15001, "protocol": "TCP"}], "resources": {}})
        statuses = []
        phase = "Running"
        for c in conts:
            roll = rnd.random()
            st = {"name": c["name"], "image": c["image"], "restartCount": 0, "ready": True, "started": True}
            if roll < 0.15:
                st.update(ready=False, started=False, restartCount=rnd.randint(4, 40),
                          state={"waiting": {"reason": "CrashLoopBackOff", "message": "back-off 5m0s restarting failed container"}},
                          lastState={"terminated": {"exitCode": rnd.choice([1, 137]), "reason": rnd.choice(["Error", "OOMKilled"])}})
            elif roll < 0.25:
                st.update(ready=False, restartCount=0, started=False, state={"waiting": {"reason": "ImagePullBackOff"}})
                phase = "Pending"
            else:
                st.update(restartCount=rnd.choice([0, 0, 0, 1, 2]), state={"running": {"startedAt": stamp(39, rnd.randint(0, 86399))[:-5] + "Z"}})
            statuses.append(st)
        pod = {"apiVersion": "v1", "kind": "Pod",
               "metadata": {"name": name, "namespace": ns, "labels": {"app": app, "pod-template-hash": suffix[:5]},
                            "creationTimestamp": stamp(rnd.randint(30, 40), rnd.randint(0, 86399))[:-5] + "Z",
                            "uid": "%08x-%04x-%04x-%04x-%012x" % (rnd.getrandbits(32), rnd.getrandbits(16), rnd.getrandbits(16), rnd.getrandbits(16), rnd.getrandbits(48))},
               "spec": {"containers": conts, "nodeName": rnd.choice(nodes), "restartPolicy": "Always"},
               "status": {"phase": phase, "podIP": "10.244.%d.%d" % (rnd.randint(0, 3), rnd.randint(2, 250)),
                          "containerStatuses": statuses, "qosClass": rnd.choice(["Burstable", "BestEffort", "Guaranteed"])}}
        if app == "prometheus":
            pod["metadata"]["annotations"] = {"prometheus.io/scrape": "true", "prometheus.io/port": "9090"}
        pods.append(pod)
wj("k8s/pods.json", {"apiVersion": "v1", "items": pods, "kind": "List", "metadata": {"resourceVersion": ""}}, indent=4)

# ---------------------------------------------------------------- GitHub
titles = ["Crash when the config file is empty", "Support for ARM64 builds", "Typo in README",
          "Ünicode file names break the uploader", "Timeout on large uploads", "Add retry with backoff",
          "Docs: explain the --query flag", "Memory grows without bound in watch mode", "日本語のファイル名が化ける",
          "Release 2.4.0", "Flaky test: test_resume_after_disconnect", "Allow configuring the cache directory",
          "Panic on Windows paths with a trailing slash", "Bump dependency to fix advisory", "Feature: dark mode for the dashboard",
          "Wrong exit code when no files match", "Progress bar overflows on narrow terminals", "Add JSON output",
          "Login fails behind a proxy", "Deprecate the v1 API"]
users = ["octo-dev", "mlee", "a-nakamura", "rsingh", "jo-ellis", "dependabot[bot]"]
LABELS = [("bug", "d73a4a"), ("enhancement", "a2eeef"), ("documentation", "0075ca"), ("good first issue", "7057ff"),
          ("help wanted", "008672"), ("windows", "fbca04"), ("release", "ededed"), ("dependencies", "0366d6")]
issues = []
for i, t in enumerate(titles):
    num = 1480 - i * rnd.randint(1, 9)
    labs = rnd.sample(LABELS, rnd.choice([0, 1, 1, 2, 3]))
    iss = {"number": num, "title": t, "state": rnd.choice(["open", "open", "closed"]),
           "user": {"login": "dependabot[bot]" if t.startswith("Bump") else rnd.choice(users[:5]), "type": "User"},
           "labels": [{"name": a, "color": b, "default": a in ("bug", "enhancement", "documentation")} for a, b in labs],
           "assignees": [{"login": u} for u in rnd.sample(users[:5], rnd.choice([0, 0, 1, 2]))],
           "comments": rnd.choice([0, 0, 1, 3, 7, 12, 31]),
           "created_at": stamp(rnd.randint(0, 40), rnd.randint(0, 86399))[:-5] + "Z",
           "closed_at": None, "milestone": None,
           "reactions": {"total_count": 0, "+1": rnd.choice([0, 0, 1, 4, 19]), "-1": rnd.choice([0, 0, 1]), "heart": rnd.choice([0, 2])},
           "body": rnd.choice([None, "", "Steps to reproduce:\n1. run it\n2. see the error", "See #%d." % (num - 3)])}
    iss["reactions"]["total_count"] = iss["reactions"]["+1"] + iss["reactions"]["-1"] + iss["reactions"]["heart"]
    if iss["state"] == "closed":
        iss["closed_at"] = "2026-10-1%dT09:00:00Z" % rnd.randint(0, 8)
    if rnd.random() < 0.3:
        iss["pull_request"] = {"url": "https://api.github.com/repos/acme/uploader/pulls/%d" % num, "merged_at": None}
    if rnd.random() < 0.3:
        iss["milestone"] = {"title": rnd.choice(["2.4.0", "2.5.0"]), "due_on": None}
    issues.append(iss)
wj("github/issues.json", issues, indent=2)

# ---------------------------------------------------------------- odd keys
wj("config/odd-keys.json", {
    "app.name": "uploader", "with space": [1, 2, 3], "": "empty key", "日本": {"東京": 13960000},
    "quote\"key": True, "back\\slash": None, "tab\tkey": 1.5, "0": "zero", "-1": "minus one",
    "nested": {"a-b": {"c.d": [{"e f": 1}, {"e f": 2}]}}, "emoji": "rocket 🚀", "café": "naïve",
})

# ---------------------------------------------------------------- jobs
jobs = []


def job(*a):
    jobs.append(list(a))


for f in SUITE:
    job("suite", "suite/" + f)

EC2 = "aws/ec2-describe-instances.json"
S3 = "aws/s3-list-objects-v2.json"
CW = "aws/cloudwatch-cpu.json"
IAMP = "aws/iam-list-policies.json"
IAMD = "aws/iam-policy-document.json"
PODS = "k8s/pods.json"
GH = "github/issues.json"
ODD = "config/odd-keys.json"
for e in [
    "Reservations[].Instances[].InstanceId",
    "Reservations[*].Instances[*].InstanceId",
    "Reservations[].Instances[?State.Name=='running'].[InstanceId, InstanceType, PrivateIpAddress]",
    "Reservations[].Instances[].{id: InstanceId, type: InstanceType, az: Placement.AvailabilityZone, name: Tags[?Key=='Name'] | [0].Value}",
    "Reservations[].Instances[] | length(@)",
    "length(Reservations[].Instances[?State.Name=='stopped'][])",
    "Reservations[].Instances[?PublicIpAddress].PublicIpAddress",
    "Reservations[].Instances[?PublicIpAddress != null] | [].[InstanceId, PublicDnsName]",
    "Reservations[].Instances[] | sort_by(@, &LaunchTime)[-3:].[InstanceId, LaunchTime]",
    "Reservations[].Instances[] | max_by(@, &LaunchTime).InstanceId",
    "Reservations[].Instances[] | min_by(@, &CpuOptions.CoreCount).[InstanceId, CpuOptions]",
    "Reservations[].Instances[].Tags[?Key=='env'].Value[]",
    "Reservations[].Instances[?Tags[?Key=='env' && Value=='prod']].InstanceId",
    "Reservations[].Instances[?!not_null(Tags)].InstanceId",
    "Reservations[].Instances[].Tags[?starts_with(Key, 'aws:')][].Value",
    "Reservations[].Instances[].BlockDeviceMappings[].Ebs.VolumeId",
    "sum(Reservations[].Instances[].CpuOptions.[CoreCount][])",
    "sum(Reservations[].Instances[].length(BlockDeviceMappings))",
    "Reservations[].Instances[].SecurityGroups[].GroupName | sort(@)",
    "Reservations[].Instances[].[InstanceType] | [] | sort(@)",
    "Reservations[].{reservation: ReservationId, count: length(Instances), types: Instances[].InstanceType}",
    "Reservations[0].Instances[0]",
    "Reservations[-1].Instances[-1].State",
    "Reservations[].Instances[].Architecture | join(', ', @)",
    "Reservations[].Instances[?contains(InstanceType, 'g.')].InstanceId",
    "Reservations[].Instances[?Monitoring.State=='enabled' && State.Code==`16`].InstanceId",
    "Reservations[].Instances[?State.Code > `16`].[InstanceId, State.Name]",
    "Reservations[].Instances[].CpuOptions.CoreCount * ThreadsPerCore",
    "Reservations[].Instances[].Tags",
    "Reservations[].Instances[].Tag[?Key=='Name'].Value",
    "Reservations[].Instances[].Tags[?Key=='Name'].Values",
    "Reservations[].Instances[?State.Name=='running'].{Name: Tags[?Key=='Name'].Value | [0], Ip: PrivateIpAddress} | sort_by(@, &Ip)",
    "Reservations[].Instances[].length(Tags)",
    "length(Reservations[].Instances[].Tags)",
    "Reservations[].Instances[] | group_by(@, &InstanceType)",
    "Reservations[].Instances[].InstanceId | join(\" \", @)",
    "Reservations[].Instances[].InstanceId | join(' ', @",
    "Reservations[].Instances[].{Id: InstanceId, Type: InstanceType",
    "Reservations[].Instances[?State.Name=running].InstanceId",
    "Reservations[].Instances[?State.Name==`running`].InstanceId",
    "Reservations[].Instances[] | sort_by(@, &Tags)",
    "Reservations[].Instances[] | sort_by(@, &CpuOptions.CoreCount)[].[CpuOptions.CoreCount, InstanceId]",
    "reverse(Reservations[].Instances[].AmiLaunchIndex)",
    "Reservations[].Instances[].Placement.AvailabilityZone | sort(@) | [0], [-1]",
]:
    job("jp", EC2, e)
for e in [
    "Contents[].Key",
    "Contents[?Size > `1000000`].[Key, Size]",
    "sum(Contents[].Size)",
    "length(Contents)",
    "Contents[?starts_with(Key, 'logs/2026/10/')].Key",
    "Contents[?ends_with(Key, '.png') || ends_with(Key, '.jpg')] | length(@)",
    "Contents[?StorageClass=='GLACIER'].{key: Key, size: Size, modified: LastModified}",
    "max_by(Contents, &Size).Key",
    "min_by(Contents, &LastModified).[Key, LastModified]",
    "sort_by(Contents, &Size)[-5:].Key",
    "reverse(sort_by(Contents, &LastModified))[:3].[LastModified, Key]",
    "avg(Contents[?starts_with(Key, 'images/')].Size)",
    "Contents[?contains(Key, 'über')].Key",
    "Contents[?Size == `0`].Key",
    "map(&Size, Contents[?starts_with(Key, 'backups/')])",
    "map(&length(Key), Contents)[:10]",
    "Contents[].ETag | [:3]",
    "{bucket: Name, keys: KeyCount, truncated: IsTruncated, biggest: max(Contents[].Size)}",
    "Contents[?Size > `1000000000`] | sum(@[].Size) / `1073741824`",
    "Contents[*].StorageClass | sort(@) | [0:-1:7]",
    "Contents[?StorageClass != 'STANDARD'] | length(@)",
    "Contents[?LastModified >= '2026-10-01'].Key",
    "Contents[?Key < 'images/'] | [].Key",
    "Contents[].Size | max(@) - min(@)",
    "Contents[].to_string(Size) | [:4]",
    "sort(Contents[].StorageClass) | unique(@)",
    "Contents[?to_number(Size) > `500000`] | length(@)",
    "Contents[?Size > '1000'].Key",
]:
    job("jp", S3, e)
for e in [
    "Datapoints[].Average",
    "sum(Datapoints[].Average)",
    "avg(Datapoints[].Average)",
    "max(Datapoints[].Maximum)",
    "min(Datapoints[].Minimum)",
    "sort_by(Datapoints, &Timestamp)[].[Timestamp, Average]",
    "sort_by(Datapoints, &Average)[-1]",
    "Datapoints[?Average > `80`].{t: Timestamp, avg: Average}",
    "length(Datapoints[?Maximum > `90.0`])",
    "Datapoints[].floor(Average)",
    "Datapoints[].ceil(Maximum) | sort(@)",
    "sum(Datapoints[].SampleCount)",
    "Datapoints[].abs(`-1` * Average) | [:3]",
    "{label: Label, peak: max(Datapoints[].Maximum), mean: avg(Datapoints[].Average), samples: sum(Datapoints[].SampleCount)}",
    "sum(Datapoints[].Unit)",
    "Datapoints[0].to_number(to_string(Average))",
]:
    job("jp", CW, e)
for e in [
    "Policies[?AttachmentCount == `0`].PolicyName",
    "Policies[?AttachmentCount > `0`].{name: PolicyName, used: AttachmentCount}",
    "Policies[].Arn",
    "sort_by(Policies, &CreateDate)[].[CreateDate, PolicyName]",
    "Policies[?contains(PolicyName, 'Access')].Arn",
    "sum(Policies[].AttachmentCount)",
    "Policies[].DefaultVersionId | sort(@)",
]:
    job("jp", IAMP, e)
for e in [
    "PolicyVersion.Document.Statement[].Effect",
    "PolicyVersion.Document.Statement[?Effect=='Deny'].Action",
    "PolicyVersion.Document.Statement[].Action[]",
    "PolicyVersion.Document.Statement[].to_array(Action)[]",
    "PolicyVersion.Document.Statement[].Sid",
    "PolicyVersion.Document.Statement[].not_null(Sid, 'unnamed')",
    "PolicyVersion.Document.Statement[?Condition].Condition.*.*[]",
    "PolicyVersion.Document.Statement[?contains(to_array(Resource), '*')].Sid",
    "PolicyVersion.Document.Statement[?contains(to_array(Action), 's3:PutObject')] | [0].Resource",
    "PolicyVersion.Document.Statement[].{sid: Sid, actions: length(to_array(Action)), type: type(Action)}",
    "PolicyVersion.Document.Statement[*].Condition.StringEquals.\"s3:x-amz-acl\"",
    "PolicyVersion.Document.Statement[].keys(@)",
    "keys(PolicyVersion.Document.Statement[2].Condition)",
    "PolicyVersion.Document.Statement[].Action[?starts_with(@, 'kms:')][]",
    "PolicyVersion.Document.Statement[].contains(Action, 's3:GetObject')",
    "merge(PolicyVersion, {Document: 'redacted'})",
    "PolicyVersion.Document.Statement[].Resource | [] | sort(@)",
]:
    job("jp", IAMD, e)
for e in [
    "items[].metadata.name",
    "items[].[metadata.namespace, metadata.name, status.phase]",
    "items[?status.phase!='Running'].metadata.name",
    "items[?metadata.namespace=='shop'].spec.containers[].image",
    "items[].spec.containers[].image | sort(@)",
    "items[].status.containerStatuses[?!ready].name",
    "items[].status.containerStatuses[?restartCount > `3`].[name, restartCount, state.waiting.reason]",
    "items[].status.containerStatuses[].state.*.reason | []",
    "items[].{pod: metadata.name, restarts: sum(status.containerStatuses[].restartCount)} | sort_by(@, &restarts) | reverse(@)[:4]",
    "items[?length(spec.containers) > `1`].metadata.name",
    "items[].spec.nodeName | sort(@)",
    "items[?spec.nodeName=='ip-10-0-3-9.eu-west-1.compute.internal'].metadata.name",
    "items[].metadata.labels.app",
    "items[].metadata.annotations",
    "items[].metadata.annotations.\"prometheus.io/port\"",
    "items[].spec.containers[].resources.requests.memory",
    "items[].spec.containers[].ports[].containerPort | sort(@)",
    "items[].status.containerStatuses[].lastState.terminated.reason",
    "items[].status.qosClass | join(',', @)",
    "items[].spec.containers[?name=='envoy'][].image | [0]",
    "items[] | [?status.phase=='Pending'] | length(@)",
    "items[].status.containerStatuses[] | [?state.running].name | length(@)",
    "items[*].metadata.{name: name, created: creationTimestamp} | sort_by(@, &created) | [0]",
    "items[?metadata.labels.app=='coredns'].status.podIP",
    "items[].metadata.labels.\"pod-template-hash\" | [:3]",
    "items[].metadata.labels.pod-template-hash",
    "items[].status.containerStatuses[].restartCount | max(@)",
    "length(items[].spec.containers[])",
    "items[0].spec.containers[0].resources",
    "items[].spec.containers[].resources.limits.memory | [?@ == '1Gi'] | length(@)",
]:
    job("jp", PODS, e)
for e in [
    "[].number",
    "[?state=='open'].[number, title]",
    "[?pull_request == null && state=='open'].number",
    "[?pull_request].number",
    "[].labels[].name | sort(@)",
    "[?labels[?name=='bug']].title",
    "[?contains(labels[].name, 'bug')].title",
    "[].{n: number, by: user.login, labels: join(',', labels[].name)}",
    "[?user.login=='dependabot[bot]'].title",
    "sort_by(@, &comments)[-3:].[number, comments]",
    "max_by(@, &reactions.\"+1\").[number, title, reactions.\"+1\"]",
    "[?reactions.\"+1\" > `0`] | sort_by(@, &reactions.\"+1\") | reverse(@) | [].number",
    "sum([].reactions.total_count)",
    "[].reactions.+1",
    "[?milestone.title=='2.4.0'].number",
    "[?assignees].{n: number, who: assignees[].login}",
    "[?!assignees].number",
    "[?closed_at].closed_at | sort(@)",
    "[?body].body | length(@)",
    "[?length(title) > `30`].title",
    "[].length(title)",
    "[?starts_with(title, 'Docs') || starts_with(title, 'Feature')].title",
    "[].title | sort(@) | [:5]",
    "[].title | reverse(sort(@))[0]",
    "[].user.login | sort(@) | join(' ', @)",
    "[?state=='closed'] | length(@)",
    "{open: length([?state=='open']), closed: length([?state=='closed']), comments: sum([].comments)}",
    "[].labels[?default].name[]",
    "[0:5].[number, state]",
    "[::-4].number",
    "[].[number, title][?contains([1], 'Ü')]",
    "[?contains(title, 'Ü') || contains(title, '日本')].title",
    "[].reverse(title)[:2]",
]:
    job("jp", GH, e)
for e in [
    "\"app.name\"",
    "app.name",
    "\"with space\"[1]",
    "\"\"",
    "日本",
    "\"日本\".\"東京\"",
    "\"quote\\\"key\"",
    "\"back\\\\slash\"",
    "\"tab\\tkey\"",
    "\"0\"",
    "\"-1\"",
    "nested.\"a-b\".\"c.d\"[].\"e f\"",
    "keys(@)",
    "values(@)[:4]",
    "emoji",
    "length(emoji)",
    "reverse(emoji)",
    "\"café\"",
    "to_string(@)",
    "type(\"tab\\tkey\")",
    "\"tab\\qkey\"",
    "\"\\u65e5\\u672c\".*",
    "@.\"0\"",
    "@[0]",
    "`\"plain\"`",
    "`plain old string`",
    "'it''s'",
    "'it\\'s'",
    "`{\"a\": [1, 2.5, true, null]}`.a",
    "`[1, 2, 3`",
    "\"unclosed",
    "foo = bar",
    "",
]:
    job("jp", ODD, e)

# ---------------------------------------------------------------- random expressions
FIELDS = ["a", "b", "c", "name", "tags", "items", "n", "x", "nested", "list", "s", "empty", "nil", "nums", "words", "objs"]
LITS = ["`1`", "`0`", "`-2`", "`2.5`", "`true`", "`false`", "`null`", "`\"a\"`", "`[]`", "`{}`", "`[1, 2]`",
        "`{\"a\": 1}`", "'b'", "'x y'", "''", "`\"\"`", "`3.0`", "`10`"]
FUNCS1 = ["abs", "avg", "ceil", "floor", "length", "keys", "values", "max", "min", "reverse", "sort", "sum",
          "to_array", "to_string", "to_number", "type", "not_null"]
FUNCS2 = ["contains", "ends_with", "starts_with", "join", "merge", "not_null"]
FUNCSX = ["sort_by", "min_by", "max_by"]
fz = random.Random(1019)


def atom():
    r = fz.random()
    if r < 0.55:
        return fz.choice(FIELDS)
    if r < 0.75:
        return fz.choice(LITS)
    if r < 0.85:
        return "@"
    return "\"%s\"" % fz.choice(FIELDS)


def gen(d):
    if d <= 0:
        return atom()
    k = fz.randint(0, 21)
    if k == 0:
        return "%s.%s" % (gen(d - 1), fz.choice(FIELDS))
    if k == 1:
        return "%s[%d]" % (gen(d - 1), fz.randint(-3, 3))
    if k == 2:
        parts = [fz.choice(["", str(fz.randint(-3, 3))]) for _ in range(3)]
        if fz.random() < 0.5:
            return "%s[%s:%s]" % (gen(d - 1), parts[0], parts[1])
        return "%s[%s:%s:%s]" % (gen(d - 1), parts[0], parts[1], fz.choice(["", "1", "2", "-1", "-2"]))
    if k == 3:
        return "%s[*].%s" % (gen(d - 1), gen(d - 1))
    if k == 4:
        return "%s[].%s" % (gen(d - 1), fz.choice(FIELDS))
    if k == 5:
        return "%s[]" % gen(d - 1)
    if k == 6:
        return "%s[?%s]" % (gen(d - 1), gen(d - 1))
    if k == 7:
        return "%s.*" % gen(d - 1)
    if k == 8:
        return "[%s]" % ", ".join(gen(d - 1) for _ in range(fz.randint(1, 3)))
    if k == 9:
        return "{%s}" % ", ".join("%s: %s" % (fz.choice(FIELDS), gen(d - 1)) for _ in range(fz.randint(1, 3)))
    if k == 10:
        return "%s | %s" % (gen(d - 1), gen(d - 1))
    if k == 11:
        return "%s || %s" % (gen(d - 1), gen(d - 1))
    if k == 12:
        return "%s && %s" % (gen(d - 1), gen(d - 1))
    if k == 13:
        return "!%s" % gen(d - 1)
    if k == 14:
        return "%s %s %s" % (gen(d - 1), fz.choice(["==", "!=", "<", "<=", ">", ">="]), gen(d - 1))
    if k == 15:
        return "(%s)" % gen(d - 1)
    if k == 16:
        return "%s(%s)" % (fz.choice(FUNCS1), gen(d - 1))
    if k == 17:
        return "%s(%s, %s)" % (fz.choice(FUNCS2), gen(d - 1), gen(d - 1))
    if k == 18:
        return "%s(%s, &%s)" % (fz.choice(FUNCSX), gen(d - 1), gen(d - 1))
    if k == 19:
        return "map(&%s, %s)" % (gen(d - 1), gen(d - 1))
    if k == 20:
        return "%s.[%s]" % (gen(d - 1), gen(d - 1))
    return "%s.{k: %s}" % (gen(d - 1), gen(d - 1))


BREAK = list("[]{}().,:|&!=<>`'\"*@?-0 ")
exprs = []
while len(exprs) < 320:
    e = gen(fz.randint(1, 4))
    if fz.random() < 0.22:
        cs = list(e)
        p = fz.randrange(len(cs) + 1)
        if fz.random() < 0.5 and cs:
            del cs[min(p, len(cs) - 1)]
        else:
            cs.insert(p, fz.choice(BREAK))
        e = "".join(cs)
    if "\\" in e or len(e) > 160:
        continue
    exprs.append(e)
w("fuzz/expressions.jsonl", "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in exprs))
wj("fuzz/doc.json", {
    "a": {"b": {"c": [1, 2, 3]}, "name": "alpha", "n": 3},
    "b": [{"a": 1, "name": "x"}, {"a": 2.5, "name": "y"}, {"a": None}, {"name": "z", "tags": ["t1"]}],
    "c": [[1, 2], [3, [4, 5]], [], "s", None],
    "name": "doc", "tags": ["red", "green", "blue", "green"], "items": [{"n": 2}, {"n": -1}, {"n": 0.5}, {"x": 1}],
    "n": -7, "x": 2.0, "nested": {"list": [{"x": [1]}, {"x": [2, 3]}], "s": "", "empty": {}},
    "list": [3, 1, 2], "s": "hello", "empty": [], "nil": None, "nums": [4, -2.5, 10, 0, 7],
    "words": ["pear", "apple", "fig", "Banana"], "objs": [{"k": "b", "v": 2}, {"k": "a", "v": 1}, {"k": "c", "v": 3}],
})
for e in ["{x: name n: n}", "length(tags words)", "[items][0][1:3].n", "[items][0] | [1:3].n"]:
    job("jp", "fuzz/doc.json", e)
job("fuzz", "fuzz/doc.json", "fuzz/expressions.jsonl")

w("jobs.jsonl", "".join(json.dumps(j, ensure_ascii=False) + "\n" for j in jobs))
print("%d jobs, %d random expressions" % (len(jobs), len(exprs)))
