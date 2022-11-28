# Argo Rollouts Basic Concepts

## A Rollout

A **Rollout** is a Kubernetes workload resource which is equivalent to a Kubernetes Deployment object. It is intended to replace a Deployment object in scenarios when more advanced deployment or progressive delivery functionality is needed. A Rollout provides the following features which a Kubernetes Deployment cannot:

 - blue-green deployments
 - canary deployments
 - integration with ingress controllers and service meshes for advanced traffic routing
 - integration with metric providers for blue-green & canary analysis
 - automated promotion or rollback based on successful or failed metrics


---
## Ingress/Service

This is the mechanism that allows traffic from live users to enter your cluster and be redirected to the appropriate version. Argo Rollouts use the standard Kubernetes *Service* resource, but with some extra metadata needed for management.

Argo Rollouts is very flexible on networking options. First of all you can have different services during a Rollout, that go only to the new version, only to the old version or both. Specifically for Canary deployments, Argo Rollouts supports several service mesh and ingress solutions for splitting traffic with specific percentages instead of simple balancing based on pod counts and it is possible to use multiple routing providers simultaneously.

---

## An Analysis

Argo Rollouts provides several ways to perform analysis to drive progressive delivery. This allows us to  achieve various forms of progressive delivery, varying the point in time analysis is performed, it's frequency, and occurrence.

An analysis is enabled by the following custom resources:

- An *AnalysisTemplate* is a template spec which defines how to perform a canary analysis, such as the metrics which it should perform, its frequency, and the values which are considered successful or failed. AnalysisTemplates may be parameterized with input values

- An *AnalysisRun* is an instantiation of an AnalysisTemplate. AnalysisRuns are like Jobs in that they eventually complete. Completed runs are considered Successful, Failed, or Inconclusive, and the result of the run affect if the Rollout's update will continue, abort, or pause, respectively.

---
## An Experiment
 
An *Experiment* is a limited run of one or more ReplicaSets for the purposes of analysis. Experiments typically run for a pre-determined duration, but can also run indefinitely until stopped. 

Experiments may reference an AnalysisTemplate to run during or after the experiment. 

The canonical use case for an Experiment is to start a baseline and canary deployment in parallel, and compare the metrics produced by the baseline and canary pods for an equal comparison.

---

## Explore Argo Rollouts 

Let's see what Argo Rollouts components we have in our cluster
.exercise[
  ```bash
  kubectl get all -n argo-rollouts
  ```
]

And the custom resources used to configure the rollouts.

.exercise[
  ```bash
  kubectl get crds | grep argo
  ```
]

