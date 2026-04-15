# qos-reliability


## Quick intuition
Reliable = “Do not lose messages.”
Best effort = “Do not slow down for lost messages.”


## Reliable

With reliable QoS, the middleware tries hard to make sure messages arrive. That means the publisher expects acknowledgements from matching subscribers and may retransmit data that was not received properly. ROS 2 docs describe this as the mode that can behave more like TCP.

What that means in practice:

Better when every message matters
More network overhead
Can increase latency under bad network conditions
Can cause backpressure or slower progress if the network is lossy or subscribers cannot keep up
Useful for commands, state changes, important events, configuration, mission-critical data

A good mental model is:

“I would rather wait a bit and get the message than lose it.”

Examples:

Robot mode change
Goal commands
Safety-related status
A map update that should not be silently dropped


## Best effort

With best effort QoS, the middleware sends messages without guaranteeing delivery. Lost packets are just lost. ROS 2 docs compare this to a UDP-like mode.

What that means in practice:

Lower overhead
Lower latency
Better for high-rate streams where old data quickly becomes useless
More tolerant of lossy wireless links
Good when getting the latest sample matters more than getting every sample

A good mental model is:

“Just give me the newest data you can; don’t waste time retrying old data.”

Examples:

Camera images
LiDAR scans
IMU data
Fast telemetry where missing one frame is acceptable

That is why ROS 2’s predefined SensorDataQoS uses best effort, keep_last, and a small depth by default.

Reliable vs best effort: the tradeoff

The core tradeoff is:

Reliable: correctness/completeness first
Best effort: timeliness/freshness first

## Compatability

QoS compatibility matters a lot in ROS 2. A publisher and subscriber will only connect if their policies are compatible. For reliability, a reliable subscriber cannot be satisfied by a best-effort publisher, while a best-effort subscriber can generally connect to a reliable publisher because the publisher is offering at least that level of service.

So in practice:

Publisher reliable + subscriber reliable → connects
Publisher reliable + subscriber best effort → usually connects
Publisher best effort + subscriber best effort → connects
Publisher best effort + subscriber reliable → not compatible

This is a very common reason for “why isn’t my subscriber receiving messages?”

## How to choose

A good rule of thumb:

### Use reliable when:

Every message matters
Topic rate is moderate or low
Retransmission cost is acceptable
You are sending commands, decisions, or important state

### Use best effort when:

Topic rate is high
Data gets stale quickly
Some loss is acceptable
You are on Wi-Fi, lossy links, or streaming sensor data
