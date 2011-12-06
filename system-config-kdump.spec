Summary: A graphical interface for configuring kernel crash dumping
Name: system-config-kdump
Version: 2.0.2.2
Release: 2%{?dist}
URL: http://fedorahosted.org/system-config-kdump/
License: GPLv2+
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Source0: http://fedorahosted.org/released/system-config-kdump/%{name}-%{version}.tar.bz2
ExcludeArch: s390 s390x
BuildRequires: desktop-file-utils
BuildRequires: intltool, gettext, gnome-doc-utils, docbook-dtds, rarian-compat, scrollkeeper
Requires: pygtk2 >= 2.8.6
Requires: pygtk2-libglade
Requires: usermode >= 1.36
Requires: kexec-tools
Requires: yelp
Requires: python-slip-dbus
Requires(pre): gtk2 >= 2.8.20
Requires(pre): hicolor-icon-theme

# 622868, add fallback to getting total mem from /proc/meminfo
Patch1: system-config-kdump-2.0.2.2-memory.patch

%description
system-config-kdump is a graphical tool for configuring kernel crash
dumping via kdump and kexec.

%prep
%setup -q
%patch1 -p1 -b .memory

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make INSTROOT=$RPM_BUILD_ROOT install
desktop-file-install --vendor system --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --remove-category Application                             \
  --remove-category SystemSetup                             \
  --remove-category GTK                                     \
  --add-category Settings                                   \
  $RPM_BUILD_ROOT%{_datadir}/applications/system-config-kdump.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
%{_bindir}/scrollkeeper-update -q || :


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
%{_bindir}/scrollkeeper-update -q || :



%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/system-config-kdump
%{_datadir}/system-config-kdump
%{_datadir}/applications/*
%config(noreplace) %{_sysconfdir}/security/console.apps/system-config-kdump
%config(noreplace) %{_sysconfdir}/pam.d/system-config-kdump

%{_sysconfdir}/dbus-1/system.d/org.fedoraproject.systemconfig.kdump.mechanism.conf
%{_datadir}/dbus-1/system-services/org.fedoraproject.systemconfig.kdump.mechanism.service
%{_datadir}/polkit-1/actions/org.fedoraproject.systemconfig.kdump.policy

%{_datadir}/icons/hicolor/48x48/apps/system-config-kdump.png

%doc ChangeLog COPYING
%doc %{_datadir}/gnome/help/system-config-kdump
%doc %{_datadir}/omf/system-config-kdump

%changelog
* Tue Aug 10 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.2-2
- Add fallback to get total mem from /proc/meminfo
  Resolves: #622868

* Tue Aug 10 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.2-1
- Bump to 2.0.2.2
- New traslations
  Resolves: #610471

* Wed Jun 30 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-19
- Added poweroff default action
- Added missing check
  Resolves: #603801

* Wed Jun 30 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-18
- Added support for ext4
- check the return code of the service handling
- show error message when cathed dbus exception
  Resolves: #608020

* Mon Jun 07 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-17
- Calculate total memory from /proc/iomem rather than read it
  from /proc/meminfo.
  Resolves: #581422

* Tue May 25 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-16
- Properly deal with unsupported bootloader
  Resolves: #590380

* Tue May 25 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-15
- Make the apply button sensitive if the application makes a change and
  not only if the user make a change
  Resolves: #581433

* Wed May 19 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-14
- Additional checks for valid crashkernel value
  Resolves: #591019

* Wed May 19 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-13
- Show the help in the right place in yelp
  Resolves: #588576

* Wed May 19 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-12
- Added translations
  Resolves: #575679

* Mon Apr 26 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2.1-11
- Added new translations

* Thu Apr 22 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-10
- Use better policy
- Better calculation of total memory on system
  Resolves: #581422

* Thu Apr 15 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-9
- Removed deprecated text
  Resolves: #581446

* Thu Apr 15 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-8
- Do not depend on bitmap-fonts
  Resolves: #581916

* Thu Apr 08 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-7
- Use icon for main window and better name in gnome menu
  Resolves: #567680

* Thu Mar 11 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-6
- Fixed typo
  Resolves: #572219

* Wed Mar 10 2010 Roman Rakus <rrakus@redhat.com> - 2.0.2-5
- Use `auto' as default and allow to manually set size
  Resolves: #556866

* Tue Feb 09 2010 Roman Rakus <rrakus@redhat.com> 2.0.2-4
- Get a rid of rhpl
  Resolves: #563143

* Thu Jan 21 2010 Roman Rakus rrakus@redhat.com 2.0.2-3
- Inform user that he doesn't have enough memory for auto crashkernel
- Allow him to set everything but memory for kdump
  Resvoles: #556866

* Wed Jan 20 2010 Roman Rakus <rrakus@redhat.com> 2.0.2-2
- Use only auto value for crashkernel kernel argument
  Resolves: #528714
- Since auto is only valid, don't try to integerize it
  Resolves: #556866

* Mon Dec 07 2009 Roman Rakus <rrakus@redhat.com> - 2.0.2-1
- Don't be interested in non linux entries in bootloaders conf.
  Resolves: #538850

* Fri Oct 02 2009 Roman Rakus <rrakus@redhat.com> - 2.0.1-1
- Update to version 2.0.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 04 2009 Roman Rakus <rrakus@redhat.com> - 2.0.0-2
- Added missing requires python-slip-dbus

* Tue May 05 2009 Roman Rakus <rrakus@redhat.com> - 2.0.0-1
- Changed to satisfy system config tools clenaup

* Mon Apr 13 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.0.14-6
- Improve error handling when applying settings

* Mon Mar 23 2009 Roman Rakus <rrakus@redhat.com> - 1.0.14-5
- Fix off by one error in kernel command line parsing
  Resolves #334269

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.14-3
- Rebuild for Python 2.6

* Thu Sep 11 2008 Roman Rakus <rrakus@redhat.com> 1.0.14-2
- Don't specify any offset in cmdline argument
  Resolves: #461602

* Tue Sep 09 2008 Roman Rakus <rrakus@redhat.com> 1.0.14-1
- Bump to version 1.0.14

* Fri Feb 01 2008 Dave Lehman <dlehman@redhat.com> 1.0.13-2%{?dist}
- replace desktop file category "SystemSetup" with "Settings"

* Fri Jan 18 2008 Dave Lehman <dlehman@redhat.com> 1.0.13-1%{?dist}
- handle kdump service start/stop
  Resolves: rhbz#239324
- only suggest reboot if memory reservation altered
  Related: rhbz#239324
- preserve unknown config options
  Resolves: rhbz#253603
- add 'halt' default action
  Related: rhbz#253603

* Tue Oct 23 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-5%{?dist}
- fix license tag again

* Tue Oct 23 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-4%{?dist}
- fix desktop file in spec to avoid patching

* Mon Oct 22 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-3%{?dist}
- fix desktop file categories
- remove redhat-artwork requires

* Fri Oct 19 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-2%{?dist}
- change License to GPL2+

* Tue Sep 11 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-1%{?dist}
- prompt user for a PAE kernel for 32-bit xen with >4G memory (Jarod Wilson)
  Resolves: rhbz#284851

* Wed Aug 29 2007 Dave Lehman <dlehman@redhat.com> 1.0.11-1%{?dist}
- add support for xen (patch from Jarod Wilson)
  Resolves: #243191

* Tue Jan 16 2007 Dave Lehman <dlehman@redhat.com> 1.0.10-1%{?dist}
- handle ia64 bootloader correctly
  Resolves: #220231
- align memory requirements with documented system limits
  Resolves: #228711

* Wed Dec 27 2006 Dave Lehman <dlehman@redhat.com> 1.0.9-3%{?dist}
- only present ext2 and ext3 as filesystem type choices (#220223)

* Wed Dec 27 2006 Dave Lehman <dlehman@redhat.com> 1.0.9-2%{?dist}
- make "Edit Location" button translatable (#216596, again)

* Mon Dec 18 2006 Dave Lehman <dlehman@redhat.com> 1.0.9-1%{?dist}
- more translations
- use file: URIs instead of local: (#218878)

* Tue Dec  5 2006 Dave Lehman <dlehman@redhat.com> 1.0.8-1%{?dist}
- more translations (#216596)

* Wed Nov 29 2006 Dave Lehman <dlehman@redhat.com> 1.0.7-1%{?dist}
- rework memory constraints for increased flexibility (#215990)
- improve consistency WRT freezing/thawing of widgets (#215991)
- update translations (#216596)

* Fri Oct 27 2006 Dave Lehman <dlehman@redhat.com> 1.0.6-1%{?dist}
- add ChangeLog and COPYING as docs

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.5-3%{?dist}
- use %%{_sysconfdir} instead of /etc in specfile

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.5-2%{?dist}
- remove #!/usr/bin/python from system-config-kdump.py (for rpmlint)

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.5-1%{?dist}
- fix install make target to specify modes where needed
- remove unnecessary %%preun
- various specfile fixes to appease rpmlint

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.4-2
- fix path to icon in glade file

* Tue Oct 24 2006 Dave Lehman <dlehman@redhat.com> 1.0.4-1
- all location types now in combo box (no text entry for type)
- preserve comment lines from kdump.conf instead of writing config header
- add hicolor icon from Diana Fong

* Thu Oct 19 2006 Dave Lehman <dlehman@redhat.com> 1.0.3-1
- rework UI to only allow one location
- minor spec file cleanup

* Wed Oct 18 2006 Dave Lehman <dlehman@redhat.com> 1.0.2-1
- add support for "core_collector" and "path" handlers
- give choices of "ssh" and "nfs" instead of "net"
- validate results of edit location dialog
- add choice of "none" to default actions
- remove "ifc" support since it's gone from kexec-tools
- update kdump config file header
- fix a couple of strings that weren't getting translated

* Mon Oct 16 2006 Dave Lehman <dlehman@redhat.com> 1.0.1-3
- Fix parsing of "crashkernel=..." string from /proc/cmdline

* Fri Oct 13 2006 Dave Lehman <dlehman@redhat.com> 1.0.1-2
- convert crashkernel values to ints when parsing

* Tue Oct 10 2006 Dave Lehman <dlehman@redhat.com> 1.0.1-1
- Fix bugs in writeDumpConfig and writeBootloaderConfig
- Fix handling of pre-existing "ifc" and "default" directives
- Always leave network interface checkbutton sensitive
- Various minor fixes

* Fri Oct 06 2006 Dave Lehman <dlehman@redhat.com> 1.0.0-1
- Initial build

