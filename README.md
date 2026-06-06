# overthink-fedora — native RPM packaging for `ov`

`overthink.spec` builds the `overthink` RPM (the `ov` CLI at `/usr/bin/ov`) for
Fedora and the rpm-family distros.

It is consumed two ways, both through the SAME
`build.yml distro.fedora.format.rpm.local_pkg.build_template`:

- **localpkg deploy** — `ov deploy` / `ov update` / `ov eval run` to a `target:
  vm` (or `target: local`) Fedora target builds this RPM on the host (in a fedora
  container) and `dnf install`s it onto the target, auto-resolving the mandatory
  deps.
- **release artifacts** — `task pkg:fedora` builds a downloadable `.rpm` into
  `dist/`.

The spec packages a prebuilt `ov` binary passed as `%{ovbin}` and takes the
package version from the binary's own CalVer (`%{ovver}`), so `rpm -q overthink`
always matches `ov version`. Mandatory dependencies are `Requires:` (all in the
Fedora repos, including tailscale); Docker / GPU / k8s tooling is `Suggests:`.

History lives in the superproject's `CHANGELOG.md`.
