# TierProvision
# Cost Analysis in Multi Tier Cloud Architecture
  Cloud computing resources scale elastically, and hence reduce the risk of under provisioning and wastage due to over provisioning
during non-peak hours. To maximise the benefits of cloud computing, efficient dynamic resource provisioning is required. Further,
any dynamic resource scaling algorithm maybe based on a mixture of predictive scaling and reactive scaling. We seek to address the
problem of dynamic resource provisioning in cloud data centres. We aim to begin with a two-tier structure and explore the
possibility of extending it to a multi-tier cloud architecture.

  This problem is difficult because modifying the resource allocation comes with an overhead and it must not violate the SLAs
offered by the Cloud Provider. Moreover, the machines in different tiers have different resource capacities, initialization
overheads, latencies and expenses and hence load balancing is not straightforward. The provisioning algorithm must choose a tier to
de-allocate or allocate an instance such that the SLO is maintained and an optimal amount of resources are utilised. 

  Several research efforts have been made to efficiently solve the dynamic resource allocation problem. Some algorithms use queuing
models that determine which tier to re-provision, some algorithms also factor in heterogeneity of resources in different tiers and
use profiling of machine performance to select a tier and some algorithms are designed based on low level hardware based
performance models. Finally, some methods use control theory to allocate resources rather than using predictive methods.

  We propose to start with a simple model for a two-tier structure having one parent and two children. We plan to have CPU, memory,
storage and access latencies as some of the parameters used to determine the cost of provisioning decisions. Further we plan to
extend our analysis to more than two tiers and modify and apply existing algorithms.

> _We can only see a short distance ahead, but we can see plenty there that needs to be done._ **_~Alan Turing_**
