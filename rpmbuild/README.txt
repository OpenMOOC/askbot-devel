

RPM Build guide:

You need to create a relase package with python setup sdist and copy the egg file to SOURCES.

Modify SPECS/askbot.spec according to relase and package name.

To make easy rpm build process is better

Instal rpmdevtools

 # yum install rpmdevtools

Build directory tree in your home with rpmdev-setuptree 
