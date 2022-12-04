# Progressive Delivery Defined

**Progressive Delivery** is the collective definition 
for a set of deployment techniques that allow for gradual,
reliable and low-stress release of new software versions into production environments.

Argo Rollouts allow us to automate these techniques.

Techniques we will be looking at today are:

- Blue-Green

- Canary deployments

- Traffic Mirroring

- Experiments
---

## Blue-Green

A Blue-Green deployment (sometimes referred to as a Red-Black) has both the new and old version of the application deployed at the same time. During this time, only the old version of the application will receive production traffic. This allows the developers to run tests against the new version before switching the live traffic to the new version.

![img alt=><](images/bluegreen.png)

---

## Canary Deployments

**Canary Deployments** is the process in which a new version that is released to production gets only a tiny percent of actual production traffic. While the rest of traffic continues to be served by the old version. This may cause a minimal, sufferable service disruption. If the new version functions fine - we gradually switch more traffic over to it from the old version. Until all traffic is served by the new version and the old version can be retired.

![img alt=><](images/canary.png)

---

## Traffic Mirroring
*Traffic Mirroring* (or traffic shadowing) is more of a testing technique whereas we release the new version to production and channel all the production traffic to it.
This happens in parallel to serving this traffic by the old version. 
No responses are sent back from the new version. This allows us to test the new version with full production traffic and data without impacting our users.

![img alt=><](images/mirroring.png)

---
## Experiments

**Experiments** AKA A/B Testing is also a testing technique whereas we release 2 or more versions to production and run the for a specifed period in order to analyse their performance. 

This can be a technical step in the process of either blue-green or canary rollout. 

Or it can be a stand-alone technique for verifying feature completeness of a version before release.


---

## How Can Rollouts Help

- With Argo Rollouts we can define and manage precisely:
  -  What versions of a service are rolled out
  -  The percentage of traffic routed to each version
  -  The criteria for promoting to the next stage
  -  The experiments and analysis to run at each stage

- But first let's learn the basics how Argo Rollouts work
