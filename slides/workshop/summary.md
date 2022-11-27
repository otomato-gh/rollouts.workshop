# Summing It All Up

- We've learned what a Service Mesh is

- We've learned how Istio works

- We've seen the following progressive delivery strategies:

  - Dark Launch

  - Traffic Mirroring

  - Canary Deployment

---

## Wrap-up Exercise

- Check out `final` branch of istio.workshop

.exercise[

```bash
git checkout final
```
]

- Build and push a new version of `aleph`

.exercise[

```bash
cd aleph
docker build . -t ${REGISTRY}/aleph:0.2
docker push ${REGISTRY}/aleph:0.2
```
]

---

## Wrap-up Exercise

- Create a DestinationRule for aleph in namespace `staging`:

    - With subset `production` pointing at pods with label `version=v01`
    - With subset `canary` pointing at pods with label `version=v02`

- Create a VirtualService in namespace `staging`:

    - Default route: `aleph` with subset `production`

    - Mirror traffic to subset `canary`

- Create a new deployment `aleph-v02` with labels :

    - version: v02
    - app: aleph

---

## Check Status of the New Deployment

- Generate load on aleph service

- (Hint: use the `curler` pod we've created)

- Check Graphana for aleph service stats

- Is the new version healthy?

--

- It's not! 

- Remove the deployment for `aleph v02`


---

## Let's Fix This

- Fix `aleph`. *Hint - the bug is in `version` method*

- Build version 0.3 of `aleph`

- Deploy the new version

- Expose it as a canary. Increment by 20 percent each time, verifying that all the requests are successful.

---

## That's It for Today!

- Thanks for attending!

- Any future questions: Slack or `contact@otomato.link`

- For more training : https://devopstrain.pro