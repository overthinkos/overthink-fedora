# overthink.spec — the native RPM for the `ov` CLI (Fedora / rpm-family).
#
# Built by ov's localpkg mechanism AND the release-artifact path through ONE
# shared build.yml distro.fedora.format.rpm.local_pkg.build_template: the ov
# binary is built on the HOST (prebuilt bin/ov, or a go-build fallback) and
# bind-mounted into a fedora container as the ovbin define; rpmbuild here just
# packages it. The package version is the binary's own CalVer, passed as the
# ovver define, so `rpm -q overthink` always agrees with `ov version`.
#
# Install: `dnf install ./overthink-*.rpm` AUTO-RESOLVES every mandatory dep
# below from the Fedora repos (all present, incl. tailscale). Optional/situational
# tools are Suggests: — documented, never auto-pulled.

%global debug_package %{nil}
%global __strip /bin/true

Name:           overthink
Version:        %{ovver}
Release:        1%{?dist}
Summary:        Overthink container management CLI
License:        MIT
URL:            https://github.com/overthinkos/overthink
ExclusiveArch:  x86_64

# --- Mandatory runtime deps (every repo-available tool ov invokes; Fedora names) ---
Requires:       glibc
Requires:       podman
Requires:       gocryptfs
Requires:       fuse3
Requires:       fuse-overlayfs
Requires:       slirp4netns
Requires:       openssh-clients
Requires:       openssh-server
Requires:       util-linux
Requires:       skopeo
Requires:       qemu-system-x86
Requires:       qemu-img
Requires:       virtiofsd
Requires:       libvirt
Requires:       libvirt-client
Requires:       tailscale
Requires:       bsdtar
Requires:       iproute
Requires:       xorriso
Requires:       genisoimage
Requires:       edk2-ovmf
Requires:       dnsmasq
Requires:       swtpm
Requires:       gnupg2
Requires:       pinentry

# --- Optional / situational (Suggests = documented, never auto-installed) ---
Suggests:       docker
Suggests:       cloudflared
Suggests:       gvisor-tap-vsock
Suggests:       xorg-x11-drv-nvidia-cuda
Suggests:       kubernetes-client

%description
Overthink container management CLI — compose, build, deploy, and manage
container boxes from a library of fully configurable candies. This package
ships the `ov` binary; dnf auto-resolves its mandatory dependencies.

%install
install -Dm0755 %{ovbin} %{buildroot}%{_bindir}/ov

%files
%{_bindir}/ov

%changelog
* Sat Jun 06 2026 Andreas Trawoeger <atrawog@overthink.net> - %{ovver}-1
- Native RPM for the ov CLI; version tracks the bundled binary's CalVer.
