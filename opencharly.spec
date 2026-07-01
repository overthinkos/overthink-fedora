# opencharly.spec — the native RPM for the `charly` CLI (Fedora / rpm-family).
#
# Built by charly's localpkg mechanism AND the release-artifact path through ONE
# shared build.yml distro.fedora.format.rpm.local_pkg.build_template: the charly
# binary AND the welded command plugins are built on the HOST (prebuilt bin/charly +
# the pkg/host-command-plugins.txt set, or a go-build fallback) and bind-mounted into
# a fedora container as the ovbin (charly binary) + ovplugins (plugin dir) defines;
# rpmbuild here just packages them. The package version is the binary's own CalVer,
# passed as the ovver define, so `rpm -q opencharly` always agrees with `charly version`.
#
# Install: `dnf install ./opencharly-*.rpm` AUTO-RESOLVES every mandatory dep
# below from the Fedora repos (all present, incl. tailscale). Optional/situational
# tools are Suggests: — documented, never auto-pulled.

%global debug_package %{nil}
%global __strip /bin/true

Name:           opencharly
Version:        %{ovver}
Release:        1%{?dist}
Summary:        OpenCharly container management CLI
License:        MIT
URL:            https://github.com/overthinkos/overthink
ExclusiveArch:  x86_64

# --- Mandatory runtime deps (every repo-available tool charly invokes; Fedora names) ---
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
OpenCharly container management CLI — compose, build, deploy, and manage
container boxes from a library of fully configurable candies. This package
ships the `charly` binary plus the welded command plugins beside it at
/usr/lib/charly/plugins (so `charly doctor`/`clean`/`vm`/… resolve project-less);
dnf auto-resolves its mandatory dependencies.

%install
install -Dm0755 %{ovbin} %{buildroot}%{_bindir}/charly
# The WELDED command plugins, host-built beside charly and passed in via %{ovplugins}
# (= the /ovbin/plugins bind mount the rpm build_template stages). They live beside the
# binary at /usr/lib/charly/plugins so the core `charly doctor`/`clean`/`settings`/
# `candy`/`tmux`/`preempt`/`feature`/`vm`/`secrets`/`udev` commands (each an
# out-of-process command:<word> plugin, NOT compiled in) resolve project-less on the
# installed rpm. discoverBakedPluginWords reads each `.providers` manifest at startup to
# register the word WITHOUT connecting the plugin (lazy connect on first use). Mirrors
# the arch PKGBUILD's package() baking + pkg/debian's opencharly.install, off the SAME
# pkg/host-command-plugins.txt set.
mkdir -p %{buildroot}/usr/lib/charly/plugins
for f in %{ovplugins}/*.providers; do
  p="$(basename "$f" .providers)"
  install -Dm0755 "%{ovplugins}/$p"           "%{buildroot}/usr/lib/charly/plugins/$p"
  install -Dm0644 "%{ovplugins}/$p.providers" "%{buildroot}/usr/lib/charly/plugins/$p.providers"
done

%files
%{_bindir}/charly
%dir /usr/lib/charly
/usr/lib/charly/plugins/

%changelog
* Sat Jun 06 2026 Andreas Trawoeger <atrawog@opencharly.ai> - %{ovver}-1
- Native RPM for the charly CLI; version tracks the bundled binary's CalVer.
