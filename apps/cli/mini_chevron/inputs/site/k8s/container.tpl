name: {{name}}
image: {{image}}:{{tag}}
{{#ports.0}}
ports:
{{/ports.0}}
{{#ports}}
  - containerPort: {{.}}
{{/ports}}
{{#env.0}}
env:
{{/env.0}}
{{#env}}
  - name: {{name}}
    value: "{{value}}"
{{/env}}
resources:
  limits: {cpu: "{{limits.cpu}}", memory: "{{limits.memory}}"}
