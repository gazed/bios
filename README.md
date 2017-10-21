<!-- Copyright © 2017 Galvanized Logic Inc.                       -->

# Bios

Bios is a Basic iOS application written in golang using the vu engine.
It was created to help solve the following apple itunes upload error.
The error happens when uploading bios.ipa to iTunes Connect
using Xcode Application Loader.

ERROR ITMS-90209: "Invalid Segment Alignment. The app binary at 'bios.app/bios'
does not have proper segment alignment. Try rebuilding the app with the latest Xcode version."

Build
-----

* Install the [vu](https://github.com/gazed/vu) engine first using ``go get github.com/gazed/vu``.
* Download bios into the ``src`` directory of a Go workspace which is
  any directory in the ``$GOPATH``. Using ``go get github.com/gazed/bios``
  places bios in ``$GOPATH/src/github.com/gazed/bios``.
* Test correct setup by running ``go build`` from the ``bios`` directory and then run
  the resulting ``./bios`` executable. You should see a spinning ball.
* Create and package an ios application using ``build.py clean ios`` from
  the ``bios/admin`` directory. All build output is located in the
 ``bios/admin/target`` directory.

  NOTE: iOS builds require you to to create and use your own iOS provisioning
  profiles and iOS signing certificates. See Files and Notes below.

**Developer Build Dependencies**

* go1.6+ (tested with go1.9.1)
* vu engine.

**Production Build Dependencies**

* go1.6+
* vu engine.
* python 2.7.10 for the build script.
* Xcode 9 for cross compiling.

**Runtime Dependencies**

Transitive dependencies from the ``vu`` engine.

* OpenGL version 3.3 or later for macos or windows.
* OpenGLES 3.0 for iOS

Files and Notes
---------------

iOS builds require provisioning profiles downloaded from an iOS developer account
and iOS developer signing certificates. Update ``**`` files need to match your
iOS developer information.

``
* admin/
  * ios/                          // ios build assets used by build.py.
    * assetcatalog.plist          // needed for compiling icon resources.
    * Contents.json               // needed for compiling icon resources.
    * Default-568h@2x.png         // default app icon.
    * dev.mobileprovision         ** your developer provisioning profile
    * dist.mobileprovision        ** your distribution provisioning profile
    * entitlements-dist.plist     ** update with your application and developer info.
    * entitlements.plist          ** update with your application and developer info.
    * icon_1024x1024.png          // mandatory icon.
    * icon_120x120.png            //   "        "
    * icon_167x167.png            //   "        "
    * icon_76x76.png              //   "        "
    * icon_76x76x2.png            //   "        "
    * Info.plist                  ** update with your application info.
  * target/                       // build output directory generated from build.py.
    * ios/
      * bios.app/                 // developer build for iphones,ipads.
      * bios.pkg/                 // temp distribution build zipped into bios.ipa
      * Images.xcassets/          // temp directory for compiling icon assets.
      * bios.ipa                  // distribution build for itunes connect upload.
  * build.py                      // python build script.
* images/
  * ball.png                      // texture for ball model.
* models/
  * ball.obj                      // ball model.
* source/
  * ball.fsh                      // ball model fragment shader.
  * ball.vsh                      // ball model vertex shader.
  bios.go                         // go code.
  README.md
``
