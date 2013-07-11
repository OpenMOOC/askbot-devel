%define srcname askbot
%define platform openmooc

Name:           %{platform}-%{srcname}
Version:        0.7.44
Release:        2%{?dist}
Summary:        Question and Answer forum. OpenMOOC fork.
Group:          Applications/Publishing
License:        GPLv3+
URL:            http://askbot.org
Source0:        https://github.com/OpenMOOC/askbot-devel/archive/spanish-translations.tar.gz
Source1:        askbot.wsgi
Source2:        askbot-settings.py
Source3:        askbot-httpd.conf
Source4:        README.fedora

BuildArch:      noarch
BuildRequires:  python-setuptools python-devel gettext

Requires:       Django14 Django-south
Requires:       django-keyedcache django-robots django-countries
Requires:       django-kombu django-threaded-multihost
Requires:       python-html5lib python-oauth2 python-coffin python-markdown2
Requires:       python-recaptcha-client MySQL-python python-openid python-amqplib
Requires:       python-unidecode python-httplib2 python-psycopg2 python-akismet
Requires:       python-multi-registry python-import-utils python-wordpress-xmlrpc
Requires:       django-recaptcha-works django-picklefield pystache
Requires:       django-extra-form-fields django-authenticator = 0.1.4
Requires:       python-beautifulsoup4 python-lamson python-django-longerusername
Requires:       pytz
Requires:       python-django-tinymce >= 1.5.1b1

# optional dependencies 
Requires:       django-followit django-avatar
# for building the doc
Requires:       python-sphinx
Requires:       django-celery = 3.0.17

%if 0%{?rhel}
Requires:       python-dateutil15
%else
Requires:       python-dateutil
%endif

# We must the system askbots if it's installed
Conflicts:      askbot

%description
Question and answer forum written in python and django.

Features:
::":
   * standard Q&A functionality including votes, reputation system, etc.
   * user levels: admin, moderator, regular, suspended, blocked
   * per-user in-box for responses & flagged items (for moderators)
   * email alerts - instant and delayed, optionally tag filtered
   * search by full text and a set of tags simultaneously
   * can import data from stack-exchange database file

%prep
%setup -q -n askbot-devel-spanish-translations

# remove empty files
rm -rf %{srcname}/doc/build/html/.buildinfo
rm -rf %{sername}/db

# remove shebang
sed -i -e '1d' %{srcname}/setup_templates/manage.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Language files; not under /usr/share, need to be handled manually
(cd %{buildroot} && find . -name 'django.?o' && find . -name 'djangojs.?o') | sed -e 's|^.||' | sed -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:' \
  >> %{srcname}.lang

# add /etc/askbot, wsgi and httpd configuration files 
install -d %{buildroot}/%{_sbindir}/
install -p -m 755 %{SOURCE1} %{buildroot}%{_sbindir}/

rm -rf  %{buildroot}/%{python_sitelib}/%{srcname}/setup_templates/{upfiles,log}
rm -rf  %{buildroot}/%{python_sitelib}/%{srcname}/upfiles

install -p -m 644 %{SOURCE2} %{buildroot}/%{python_sitelib}/%{srcname}/setup_templates/settings.py
install -d %{buildroot}/%{_sysconfdir}/%{srcname}/setup_templates
cp -r %{buildroot}/%{python_sitelib}/%{srcname}/setup_templates/* \
          %{buildroot}/%{_sysconfdir}/%{srcname}/setup_templates

install -d %{buildroot}/%{_sysconfdir}/%{srcname}/sites/ask/config
cp -r %{buildroot}/%{python_sitelib}/%{srcname}/setup_templates/* \
          %{buildroot}/%{_sysconfdir}/%{srcname}/sites/ask/config

sed -i 's/@SITENAME@/ask/g' %{buildroot}/%{_sysconfdir}/%{srcname}/sites/ask/config/settings.py
sed -i 's/postgresql_psycopg2/sqlite3/' %{buildroot}/%{_sysconfdir}/%{srcname}/sites/ask/config/settings.py
sed -i 's/@DATABASENAME@/\/var\/lib\/askbot\/ask.sqlite/g' %{buildroot}/%{_sysconfdir}/%{srcname}/sites/ask/config/settings.py

install -d %{buildroot}%{_defaultdocdir}/%{srcname}-%{version}
install -p -m 644 %{SOURCE3} %{buildroot}%{_defaultdocdir}/%{srcname}-%{version}/askbot-httpd.conf
%if 0%{?rhel}
sed -i 's/python2.7/python2.6/g' %{buildroot}%{_defaultdocdir}/%{srcname}-%{version}/askbot-httpd.conf
%endif

install -d %{buildroot}/%{_localstatedir}/log/%{srcname}
install -d %{buildroot}/%{_sharedstatedir}/%{srcname}/upfiles/ask
install -p -m 644 %{SOURCE4} .

%files -f %{srcname}.lang 
%doc LICENSE COPYING AUTHORS README.rst README.fedora
%doc %{_defaultdocdir}/%{srcname}-%{version}/askbot-httpd.conf
%{_bindir}/askbot-setup
%{_sbindir}/askbot.wsgi
%dir %{_sysconfdir}/%{srcname}
%config(noreplace)     %{_sysconfdir}/%{srcname}/setup_templates
%config(noreplace) %attr(-,apache,apache) %{_sysconfdir}/%{srcname}/sites
# %config(noreplace)     %{_sysconfdir}/httpd/conf.d/askbot.conf
%attr(-,apache,apache) %{_localstatedir}/log/%{srcname}/
%attr(-,apache,apache) %{_sharedstatedir}/%{srcname}/
%dir %{python_sitelib}/%{srcname}/
%dir %{python_sitelib}/%{srcname}/locale/
%{python_sitelib}/%{srcname}/doc
%{python_sitelib}/%{srcname}/*.py*
%{python_sitelib}/%{srcname}/bin/
%{python_sitelib}/%{srcname}/conf/
%{python_sitelib}/%{srcname}/const/
%{python_sitelib}/%{srcname}/cron
%{python_sitelib}/%{srcname}/deployment/
%{python_sitelib}/%{srcname}/shims/
%{python_sitelib}/%{srcname}/skins/
%{python_sitelib}/%{srcname}/media/
%{python_sitelib}/%{srcname}/templates/
%{python_sitelib}/%{srcname}/templatetags/
%{python_sitelib}/%{srcname}/tests/
%{python_sitelib}/%{srcname}/utils/
%{python_sitelib}/%{srcname}/views/
%{python_sitelib}/%{srcname}/setup_templates/
%{python_sitelib}/%{srcname}/mail/
%{python_sitelib}/%{srcname}/migrations/
%{python_sitelib}/%{srcname}/models/
%{python_sitelib}/%{srcname}/management/
%dir %{python_sitelib}/%{srcname}/deps/
%{python_sitelib}/%{srcname}/deps/*.py*
%{python_sitelib}/%{srcname}/deps/README
%{python_sitelib}/%{srcname}/deps/django_authopenid/
%dir %{python_sitelib}/%{srcname}/deps/livesettings/
%dir %{python_sitelib}/%{srcname}/deps/livesettings/locale/
%{python_sitelib}/%{srcname}/deps/livesettings/*.py*
%{python_sitelib}/%{srcname}/deps/livesettings/README
%{python_sitelib}/%{srcname}/deps/livesettings/temp*
%{python_sitelib}/%{srcname}/importers/
%{python_sitelib}/%{srcname}/middleware/
%{python_sitelib}/%{srcname}/migrations_api/
%{python_sitelib}/%{srcname}/patches/
%{python_sitelib}/%{srcname}/search/
%{python_sitelib}/%{srcname}/user_messages/
%{python_sitelib}/askbot*.egg-info

%dir %{python_sitelib}/group_messaging
%dir %{python_sitelib}/group_messaging/migrations
%{python_sitelib}/group_messaging/*.py*
%{python_sitelib}/group_messaging/migrations/*.py*

%changelog
* Tue Jul 9 2013 Oscar Carballal Prego <ocarballal@yaco.es> - 0.7.44-2
- Minor fixes. Removed httpd, updated some stuff.

* Thu Jan 24 2013 Antonio Perez-Aranda <aperezaranda@yaco.es> - 0.7.44-1
- update to 0.7.44
- Move askbot-httpd.conf to /usr/share/doc/askbot-version to make askbot
  compatible with virtualhost.

* Sat Jan 14 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.39-1
- update to 0.7.39
  * restored facebook login after FB changed the procedure (Evgeny)
- update to 0.7.38
  * xss vulnerability fix, issue found by Radim Řehůřek (Evgeny)
- update to 0.7.37 
  * added basic slugification treatment to question titles with 
    ``ALLOW_UNICODE_SLUGS = True`` (Evgeny)
  * added verification of the project directory name to
    make sure it does not contain a `.` (dot) symbol (Evgeny)
  * made askbot compatible with django's `CSRFViewMiddleware`
    that may be used for other projects (Evgeny)
  * added more rigorous test for the user name to make it slug safe (Evgeny)
  * made setting `ASKBOT_FILE_UPLOAD_DIR` work (Radim Řehůřek)
  * added minimal length of question title ond body
    text to live settings and allowed body-less questions (Radim Řehůřek, Evgeny)
  * allowed disabling use of gravatar site-wide (Rosandra Cuello Suñol)
  * when internal login app is disabled - links to login/logout/add-remove-login-methods are gone (Evgeny)
  * replaced setting `ASKBOT_FILE_UPLOAD_DIR` with django's `MEDIA_ROOT` (Evgeny)
  * replaced setting `ASKBOT_UPLOADED_FILES_URL` with django's `MEDIA_URL` (Evgeny)
  * allowed changing file storage backend for file uploads by configuration (Evgeny)
  * file uploads to amazon S3 now work with proper configuration (Evgeny)

* Thu Dec 22 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.36-1
- update to 0.7.36
  * bugfix and made the logo not used by default
- 0.7.35
  * Removal of offensive flags (Dejan Noveski)
  * Fixes in CSS (Byron Corrales)
  * Update of Catalan locale (Jordi Bofill)

* Sun Dec 11 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.34-1
- update to 0.7.34
  * Returned support of Django 1.2 (Evgeny)

* Thu Dec 08 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.33-1
- update to 0.7.33
  * Made on log in redirect to the forum index page by default
    and to the question page, if user was reading the question
    it is still possible to override the ``next`` url parameter
    or just rely on django's ``LOGIN_REDIRECT_URL`` (Evgeny)
  * Implemented retraction of offensive flags (Dejan Noveski)
  * Made automatic dependency checking more complete (Evgeny)

* Wed Nov 30 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.32-1
- update to 0.7.32
  * Bugfixes in English locale (Evgeny)
- 0.7.31 
  * Added ``askbot_create_test_fixture`` management command (Dejan Noveski)
  * Integrated new test fixture into the page load test cases (Dejan Noveski)
  * Added an embeddable widget for the questions list matching tags (Daniel Mican, Evgeny Fadeev, Dejan Noveski)
- 0.7.30
  * Context-sensitive RSS url (Dejan Noveski)
  * Implemented new version of skin (Byron Corrales)
  * Show unused vote count (Tomasz Zielinski)
  * Categorized live settings (Evgeny)
  * Merge users management command (Daniel Mican)
  * Added management command ``send_accept_answer_reminders`` (Evgeny)
  * Improved the ``askbot-setup`` script (Adolfo, Evgeny)
  * Merge users management command (Daniel Mican)
  * Anonymous caching of the question page (Vlad Bokov)
  * Fixed sharing button bug, css fixes for new template (Alexander Werner)
  * Added ASKBOT_TRANSLATE_URL setting for url localization(Alexander Werner)
  * Changed javascript translation model, moved from jqueryi18n to django (Rosandra Cuello Suñol)
  * Private forum mode (Vlad Bokov)
  * Improved text search query in Postgresql (Alexander Werner)
  * Take LANGUAGE_CODE from request (Alexander Werner)
  * Added support for LOGIN_REDIRECT_URL to the login app (hjwp, Evgeny)
  * Updated Italian localization (Luca Ferroni)
  * Added Catalan localization (Jordi Bofill)
  * Added management command ``askbot_add_test_content`` (Dejan Noveski)
  * Continued work on refactoring the database schema (Tomasz Zielinski)

* Tue Nov 15 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.29-1
- update to 0.7.29
  * minor bug fixes and additional tests (Evgeny, Adolfo)

* Wed Nov 09 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.27-1
- update to 0.7.27
  * implemented new version of skin (Byron Corrales)
  * show unused vote count (Tomasz Zielinski)
  * categorized live settings (Evgeny)
  * added management command ``send_accept_answer_reminders`` (Evgeny)
  * improved the ``askbot-setup`` script (Adolfo, Evgeny)
  * merge users management command (Daniel Mican)
  * anonymous caching of the question page (Vlad Bokov)
- 0.7.26 
  * added settings for email subscription defaults (Adolfo)
  * resolved duplicate notifications on posts with mentions (Evegeny)
  * added color-animated transitions when urls with hash tags are visited (Adolfo)
  * repository tags will be 'automatically added' to new releases (Evgeny)

* Tue Oct 06 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.25-1
- update to 0.7.25
  * RSS feed for individual question (Sayan Chowdhury)
  * allow pre-population of tags via ask a questions link (Adolfo)
  * make answering own question one click harder (Adolfo)
  * bootstrap mode (Adolfo, Evgeny)

* Tue Oct 04 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.24-1
- update to 0.7.24
  * made it possible to disable the anonymous user greeting altogether (Raghu Udiyar)
  * added annotations for the meanings of user levels on the "moderation" page. (Jishnu)
  * auto-link patterns - e.g. to bug databases - are configurable from settings. (Arun SAG)

* Wed Sep 28 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.23-1
- fix group and description
- update httpd configuration for upfiles
- update to 0.7.23
  * greeting for anonymous users can be changed from live settings (Hrishi)
  * greeting for anonymous users is shown only once (Rag Sagar)
  * added support for akismet spam detection service (Adolfo Fitoria)
  * added noscript message (Arun SAG)
  * support for url shortening with tinyurl on link sharing (Rtnpro)
  * allowed logging in with password and email in the place of login name (Evgeny)
  * added config settings allowing adjusting of license information (Evgeny)

* Fri Sep 02 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.22-3
- if RHEL, then depend on python-dateutil15 instead of python-dateutil
- add README.fedora and configuration files for multi-site deployment
- update wsgi, apache httpd configuration and settings.py setup template
- thanks to Toshio Kuriotami for suggesting and reviewing the changes

* Fri Sep 02 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.22-2
- fix copying of template files

* Thu Sep 01 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.22-1
- update to 0.7.22
  * removed printing of log message on missing optional media resources (Evgeny Fadeev)
  * fixed a layout bug on tags page (Evgeny Fadeev)
 
* Thu Sep 01 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.21-1
- update to 0.7.21
  * media resource incremented automatically (Adolfo Fitoria, Evgeny Fadeev)
  * first user automatically becomes site administrator (Adolfo Fitoria)
  * avatar displayed on the sidebar can be controlled with livesettings.(Adolfo Fitoria, Evgeny Fadeev)
  * avatar box in the sidebar is ordered with priority for real faces.(Adolfo Fitoria)
  * django's createsuperuser now works with askbot (Adolfo Fitoria)

* Sun Aug 28 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.20-1
- new upstream release
  * added support for login via self-hosted Wordpress site (Adolfo Fitoria)
  * allowed basic markdown in the comments (Adolfo Fitoria)
  * added this changelog (Adolfo Fitoria)
  * added support for threaded emails (Benoit Lavigne)
  * few more Spanish translation strings (Byron Corrales)
  * social sharing support on identi.ca (Rantadeep Debnath)

* Thu Aug 17 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.19-1
- new upstream bug fix release
  * fixes google plus and facebook login to work again
  * some styling improvements for questions sidebar
  * fixes moderation tab misalignment issue reported by me
  * replaces favorite by follow in questions
  * fixes follow user functions

* Thu Aug 11 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.18-1
- new upstream bugfix release includes improved notifications

* Thu Aug 11 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.17-1
- new upstream release
  * fixes issue with referencing username with capitalization differences
  * allow admins to add others as admins 
- requires django-celery 2.2.7

* Thu Aug 07 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.15-1
- new upstream release
- change upstream url
- add the new readme file to doc
- upstream dropped empty version.py file

* Thu Aug 03 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.14-1
- new upstream release.  
- upstream has renamed startforum to askbot-setup
- included copy of license and some documentation fixes
- upstream removed empty files, unnecessary executable bit and shebang in files
- drop requires on django-recaptcha since askbot uses django-recaptcha-works now

* Wed Aug 03 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.12-1
- new upstream release
- another fix for a unicode issue
- consolidate removal of empty files, executable bits and shebang in prep
- remove outdated bundled documentation

* Wed Aug 03 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.11-1
- new upstream release
- fixes a couple of minor bugs reported by me

* Mon Aug 01 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.10-1
- new upstream release
- fixes live search in response to problem reported by me
- now using django-recaptcha-works module

* Sun Jul 31 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.9-1
- new upstream release
- resolves bug in the sharing footer of answerless question reported by me

* Sun Jul 31 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.8-1
- new upstream release
- use django_openid_forms.patch from PJP
- add requires on django-picklefield and python-amqplib
- remove requires on python-grapefruit.  Module removed upstream
- drop all patches.  upstream removed bundled copy of python-openid

* Wed Jul 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.7-3
- add requires on MySQL-python. Don't remove openid

* Mon Jul 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.7-2
- changes from Praveen Kumar to fix all relevant rpmlint warnings and errors

* Thu Jul 14 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.7-1
- new upstream release.  
- split out bundled grapefruit, django recaptcha dependencies

* Sun Jun 26 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.1-1
- new upstream release

* Mon Apr 25 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.78-1
- new upstream release

* Thu Apr 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.76-1
- initial spec

