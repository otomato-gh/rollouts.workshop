# Deploying to K8s with Istio

The plan:

- Fix slowness by removing the `time.sleep(2)` line in beth/api.py

- Build new version by building `localhost:32000/beth:0.2`

- Push the new version to our internal registry

- Update `beth` deployment to serve the new version
---

## Deploying by Kill-And-Replace

.exercise[
```bash
cd alephbeth/beth
```
- Fix the code of beth/api.py in your editor of choice

```bash
docker build . -t localhost:32000/beth:0.2
docker push localhost:32000/beth:0.2
kubectl -n staging --record deploy/beth set image beth=localhost:32000/beth:0.2
```
- Verify deployment is updated

- Check Jaeger to see if slowness is resolved

]
.trivia[
    Do you know what that `--record` flag in the last command does?
]

---

## Is This the Right Way to Fix This?

- We just replaced a backend service by killing it

--

- What if it was in the middle of serving a request?

--

- Is the new version even functioning correctly? 

--

- Look at the version displayed for `beth`. It's the wrong number! 
  <br/>We have a bug!

--

- How can we do better?

