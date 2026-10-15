// A modern deployment: idle stats are deleted, keys are left as sent,
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
