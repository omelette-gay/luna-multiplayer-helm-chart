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

To keep secrets (e.g. the server password) out of values, set
`storage.mergeConfigFromExternalSecret`. The chart then creates an
[External Secrets](https://external-secrets.io) `ExternalSecret` that renders
the `config` files as templates (e.g. `{{ .server_password }}`) against keys
read from the named `SecretStore`, which must already exist in the namespace.
See [`ci/external-secret-values.yaml`](charts/luna-multiplayer/ci/external-secret-values.yaml)
for an example.

The universe and plugin PVCs are annotated with `helm.sh/resource-policy: keep`,
so uninstalling the release will not delete your game data.

## Releasing

1. Change the chart and bump `version` in `charts/luna-multiplayer/Chart.yaml`.
2. Open a PR; CI lints and renders the chart.
3. Merge to `main`. The `release` workflow packages the chart, creates a GitHub
   Release and updates the Helm repo index on the `gh-pages` branch.

### One-time setup

After the first release run creates the `gh-pages` branch, enable GitHub Pages
in the repo settings with source **Deploy from a branch** → `gh-pages` / `(root)`.
