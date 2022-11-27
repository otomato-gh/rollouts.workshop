class: pic
# What is a Service Mesh?
![death star](images/observability_attwitter.png)
<p align="center">
*Twitter microservices having a little chat* </p>
---

## What is a Service Mesh?

*The less helpful definition*

The term service mesh is used to describe the network of microservices that make up distributed buisness applications and the interactions between these services.

As such distributed applications grow in size and complexity these interactions become ever harder to analyze, predict and maintain.

Our services need to conform to contracts and protocols but expect the unexpected to occur.

![img alt=><](images/mesh.png)

---

## The Reality of Distributed Systems

 - RPC instead of local communication

 - Network is unreliable

 - Latency is unpredictable

 - Call stack depth is unknown

 - Dependency on other services(and teams)

 - Services are ephemeral (i.e : they come and go without prior notice)
 
 - Unpredictable load 
---

## Types of Failures in Distributed Systems

 - improper fallback settings when a service is unavailable

 - retry storms from improperly tuned timeouts

 - outages when a downstream dependency receives too much traffic

 - cascading failures when a SPOF crashes
---


## Resilience Patterns

 - connection pools

 - failure detectors, to identify slow or crashed hosts

 - failover strategies:

    - circuit breaking

    - exponential back-offs

 - load-balancers

 - back-pressure techniques

    - rate limiting
    
    - choke packets
---

## Additional Concerns

 - Service Discovery

 - Observability 

    - Distributed tracing

    - Log aggregation

 - Security

    - Point-to-point mutual TLS

 - Continuous Deployments

    - Traffic splitting

    - Rolling updates

---
## Progressive Delivery

- Rolling Updates

- Blue-Green

- Canary

- Dark Launch

- Traffic Mirroring (shadowing)

---
## What Is A Service Mesh?

A network of lightweight, centrally configurable proxies taking care of inter-service traffic.

The purpose of these proxies is to solve the application networking challenges.

They make application networking:

 - reliable

 - observable 
 
 - manageable

 ![img alt=><](images/mesh.png)