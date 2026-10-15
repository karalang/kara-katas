/*
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
