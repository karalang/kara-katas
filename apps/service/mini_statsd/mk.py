# Writes the two statsd config files in data/. The job list,
# data/jobs.txt, is written by hand.
import os, shutil
os.makedirs("data", exist_ok=True)
open("data/statsd-classic.js", "w").write("""/*
 * A classic deployment: graphite backend in legacy namespace,
 * three percentile thresholds and one histogram.
 */
{
  port: 8125
, mgmt_port: 8126
, graphitePort: 2003
, graphiteHost: "127.0.0.1"
, flushInterval: 5000
, percentThreshold: [90, 99.5, -10]
, histogram: [ { metric: 'api.latency', bins: [ 50, 100, 250, 'inf' ] } ]
}
""")
open("data/statsd-modern.js", "w").write("""// A modern deployment: idle stats are deleted, keys are left as sent,
// and graphite uses the new namespace with prefixes and a suffix.
{
  port: 8125,
  mgmt_port: 8126,
  graphitePort: 2003,
  graphiteHost: "127.0.0.1",
  flushInterval: 5000,
  deleteIdleStats: true,
  gaugesMaxTTL: 2,
  percentThreshold: 99.9,
  calculatedTimerMetrics: ['count', 'mean', 'upper', 'upper_99_9', 'count_ps'],
  prefixStats: 'agg',
  keyNameSanitize: false,
  graphite: {
    legacyNamespace: false,
    globalPrefix: 'acme',
    prefixCounter: '',
    prefixTimer: 't',
    globalSuffix: 'host1'
  },
  flush_counts: false
}
""")
if os.path.exists("jobs.txt"):
    shutil.copy("jobs.txt", "data/jobs.txt")
