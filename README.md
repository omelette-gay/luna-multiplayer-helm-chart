# luna-multiplayer-helm-chart

A Helm chart for [Luna Multiplayer](https://github.com/LunaMultiplayer/LunaMultiplayer),
the multiplayer server for Kerbal Space Program.

The chart is published to GitHub Pages as a Helm repository:

```
https://omelette-gay.github.io/luna-multiplayer-helm-chart
```

This repo only builds and publishes the chart. It does not deploy anything;
per-instance configuration lives wherever you consume the chart.

## Usage

### Helm

```sh
helm repo add luna-multiplayer https://omelette-gay.github.io/luna-multiplayer-helm-chart
helm install my-server luna-multiplayer/luna-multiplayer --version 1.0.0 -f values.yaml
```

### Terraform

```hcl
resource "helm_release" "luna_multiplayer" {
  name       = "my-server"
  namespace  = "luna-multiplayer"
  repository = "https://omelette-gay.github.io/luna-multiplayer-helm-chart"
  chart      = "luna-multiplayer"
  version    = "1.0.0"

  values = [file("${path.module}/luna-multiplayer-values.yaml")]
}
```

Always pin `version`.

## Configuration

See [`values.yaml`](charts/luna-multiplayer/values.yaml) for everything that
can be set. The server's XML config files are supplied under `config:`.

To keep secrets (e.g. the server password) out of values, create a Secret yourself and set `existingConfigSecret` to its
name. When the server starts, each file in the Secret is copied over the config file of the same name from `config`, so
the Secret only needs the files that contain secrets (e.g. a `GeneralSettings.xml` with the password in it). How the
Secret is made is up to you: the chart doesn't know or care, so it works with External Secrets, Sealed Secrets, SOPS or
a plain `kubectl create secret`. The Secret is read when the pod starts, so restart the pod after changing it.

The server's web server (port 8900) doesn't serve a web page. It returns the server's current status (players, vessels
and so on) as JSON, for status displays and other tools. The chart exposes it through an Ingress by default. Set
`webService.ingress.enabled: false` if you don't want it reachable.

The universe and plugin PVCs are annotated with `helm.sh/resource-policy: keep`,
so uninstalling the release will not delete your game data.

## Releasing

1. Change the chart and bump `version` in `charts/luna-multiplayer/Chart.yaml`.
2. Open a PR; CI lints and renders the chart.
3. Merge to `main`. The `release` workflow packages the chart, creates a GitHub
   Release and updates the Helm repo index on the `gh-pages` branch.

## Upgrading from 1.x

2.0.0 removes `storage.mergeConfigFromExternalSecret` and the `ExternalSecret` the chart used to create. Create the
Secret yourself, with the files that contain secrets already rendered, make sure it exists, and set `existingConfigSecret`
to its name before you upgrade. The chart used to put every config file into a Secret named
`<release>-luna-multiplayer-config`. It no longer creates or reads that one, so use a different name for yours.
