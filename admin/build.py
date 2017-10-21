#! /usr/bin/python
# Copyright (c) 2017 Galvanized Logic Inc.

"""
The build script for the bios project.
Expected to be run from this directory.
All build output placed in a local 'target' directory
"""

import glob         # pattern matching
import os           # for directory manipulation
import shlex        # run and control shell commands
import shutil       # for directory and file manipulation
import subprocess   # for calling shell commands
import sys          # command line arg parsing.

def cleanProject():
    # Remove all generated files.
    generatedOutput = ['target']
    print 'Removing generated output:'
    for gdir in generatedOutput:
        if os.path.exists(gdir):
            print '    ' + gdir
            shutil.rmtree(gdir)

def zipAssets():
    # zip the assets and put them in the target build output folder.
    # chdir to get proper resource zip file names.
    cwd = os.getcwd()
    os.chdir('..')
    subprocess.call(['zip', 'assets.zip']+glob.glob('models/*')+glob.glob('source/*')+glob.glob('images/*'))
    os.chdir(cwd)
    shutil.move('../assets.zip', 'target/assets.zip')

def buildIos():
    print 'Building ios'

    # Remove previous ios build. Create the ios application package directories.
    if os.path.exists('target/ios'):
        shutil.rmtree('target/ios')
    os.makedirs('target/ios/bios.app')
    os.makedirs('target/ios/bios.pkg/Payload')
    os.makedirs('target/ios/Images.xcassets/AppIcon.appiconset')

    # clang should be something like...
    # /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang
    clang = subprocess.check_output(shlex.split('xcrun --sdk iphoneos --find clang')).strip()
    #
    # iosdk should be something like...
    # /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS11.0.sdk
    iosdk = subprocess.check_output(shlex.split('xcrun --sdk iphoneos --show-sdk-path')).strip()

    # cross compile the executable and all its dependencies.
    # Note that CXX is used for objective-c.
    command = 'env GOOS=darwin GOARCH=arm64 CC='+clang+' CXX='+clang+''
    command += ' CGO_CFLAGS="-isysroot '+iosdk+' -arch arm64 -miphoneos-version-min=11.0"'
    command += ' CGO_LDFLAGS="-isysroot '+iosdk+' -arch arm64 -miphoneos-version-min=11.0"'
    command += ' CGO_ENABLED=1 go build -o target/ios/bios.app/bios bios'
    out, err = subprocess.Popen(command, universal_newlines=True, shell=True,
               stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print('built binary with command:')
    print(command)

    # copy assets to ios app directory.
    zipAssets() # create assets.zip
    subprocess.call(shlex.split('mv target/assets.zip target/ios/bios.app/assets.zip'))
    subprocess.call(shlex.split('xcrun copypng -compress -strip-PNG-text ios/Default-568h@2x.png target/ios/bios.app/Default-568h@2x.png'))

    # Compile the icon asset catalog.
    subprocess.call(shlex.split('cp ios/Contents.json target/ios/Images.xcassets/AppIcon.appiconset/'))
    subprocess.call(shlex.split('cp ios/icon_120x120.png target/ios/Images.xcassets/AppIcon.appiconset/'))
    subprocess.call(shlex.split('cp ios/icon_167x167.png target/ios/Images.xcassets/AppIcon.appiconset/'))
    subprocess.call(shlex.split('cp ios/icon_76x76.png target/ios/Images.xcassets/AppIcon.appiconset/'))
    subprocess.call(shlex.split('cp ios/icon_76x76x2.png target/ios/Images.xcassets/AppIcon.appiconset/'))
    subprocess.call(shlex.split('cp ios/icon_1024x1024.png target/ios/Images.xcassets/AppIcon.appiconset/'))
    subprocess.call(shlex.split('xcrun actool --output-format human-readable-text --notices --warnings --output-partial-info-plist ios/assetcatalog.plist --app-icon AppIcon --compress-pngs --enable-on-demand-resources YES --target-device iphone --target-device ipad --minimum-deployment-target 11.0 --platform iphoneos --product-type com.apple.product-type.application --compile target/ios/bios.app target/ios/Images.xcassets'))

    # Create the developer app. Provisioning profiles were taken from:
    # ~/Library/MobileDevice/Provisioning\ Profiles/(pick-a-dev-profile-for-ios/dev.mobileprovision)
    subprocess.call(shlex.split('cp ios/Info.plist target/ios/bios.app/Info.plist'))
    subprocess.call(shlex.split('cp ios/dev.mobileprovision target/ios/bios.app/embedded.mobileprovision'))
    subprocess.call(shlex.split('codesign -f --sign "iPhone Developer: Paul Ruest" --entitlements ios/entitlements.plist --timestamp=none target/ios/bios.app'))

    # Create the app store submission. Use the distribution provisioning profile
    # and the distribution entitilements. Pick a distribution provisioning profile for ios/dist.mobileprovision
    subprocess.call(shlex.split('cp -r target/ios/bios.app target/ios/bios.pkg/Payload')) 
    subprocess.call(shlex.split('cp ios/dist.mobileprovision target/ios/bios.pkg/Payload/bios.app/embedded.mobileprovision'))
    subprocess.call(shlex.split('codesign -vvv -f --sign "iPhone Distribution: Galvanized Logic Inc." --entitlements ios/entitlements-dist.plist --preserve-metadata=identifier,flags target/ios/bios.pkg/Payload/bios.app'))
    # ditto instead of zip to produce ipa recognized by file command.
    subprocess.call(shlex.split('ditto -V -c -k --norsrc target/ios/bios.pkg target/ios/bios.ipa'))

#------------------------------------------------------------------------------
# Main program picks the build target from the command line.

def usage():
    print 'Usage: build [clean] [ios]'

if __name__ == "__main__":
    options = {'clean'  : cleanProject,
               'ios'    : buildIos}
    somethingBuilt = False
    for arg in sys.argv:
        if arg in options:
            print 'Performing ' + arg
            options[arg]()
            somethingBuilt = True
    if not somethingBuilt:
        usage()


