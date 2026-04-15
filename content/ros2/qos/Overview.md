# Qos Overview

## The main QoS policies you’ll see are:

History: how many samples to store (keep_last or keep_all)
Depth: queue size when using keep_last
Reliability: reliable or best_effort
Durability: whether late-joining subscribers can get old data (volatile or transient_local)
Deadline / lifespan / liveliness: timing-related behavior and node aliveness checks