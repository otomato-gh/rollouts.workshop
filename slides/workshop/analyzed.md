# Analyzing Our Canaries

- In order to have real CD - we usually don't want to promote our rollouts manually

- But in order to roll out automatically we need some verification

- Argo Rollouts allows us to analyze our canaries based on telemetry

- It integrates with multiple telemetry providers - Prometheus, DataDog, NewRelic, CloudWatch, InfluxDB.

- Let's see how to use it with Prometheus.

---

## Deploy Prometheus

.exercise[
```bash
kubectl apply -f prometheus.yaml
```
- And an ingress for prometheus
```bash
MY_IP=$(dig +short myip.opendns.com @resolver1.opendns.com)
sed -i s/\<MY_IP\>/$MY_IP/ prometheus-ingress.yaml
kubectl apply -f prometheus-ingress.yaml
```
]

---

## A Rollout with Metrics

- We will deploy another application for analysis

- It's a bare bones Python Flask app with prometheus metrics

- One of its versions will increase a counter called `exceptions` on each healthcheck

- We'll define an AnalysisTemplate to count these execeptions.

---

## Our AnalysisTemplate

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: otoflask-exceptions
spec:
  args:
  - name: service-name
  metrics:
  - name: exceptions-count
    interval: 20s
    successCondition: result[0] <= 2.0
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus.default.svc.cluster.local:9090
        query: exceptions_total{instance="{{args.service-name}}:80"} 
```

---

## Let's deploy the Rollout

- Inspect all the resources in `~/rollouts.workshop/code/analyzedcanary.yaml`

- And deploy it all:

.exercise[
    ```bash
    kubectl apply -f ~/rollouts.workshop/code/analyzedcanary.yaml
    ```
]

---

## First version is OK

- Browse to `prom.YOUR.MACHINE.IP.nip.io:9090` and find the `exceptions_total` count

- Now let's deploy a bad version

.exercise[
    ```bash
    kar set image otoflask otoflask=otomato/prom-flask:0.2
    ```

- In one shell - watch the rollout
```bash
    kar get rollout otoflask -w
```
- In another - checkout the analysisRun
```bash
    kubectl get analysisruns -oyaml 
```
]

---

## Let's Deploy a Fix

- Next version `0.3` fixes the bug:

.exercise[
    ```bash
    kar set image otoflask otoflask=otomato/prom-flask:0.3
    ```
]

- Watch the canary get peacefully rolled out

