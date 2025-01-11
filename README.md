# Blendgit
Manage versions of Blender documents using Git

![](res/images/main.png)

## Installation
You can get Blendgit one of two ways:
A) Cloning into your Blender addons folder
B) Downloading a Zip archive from latest `master` or a release

### Option A: Clone into Blender's addons folder.
You may use your git client of choice to clone this repository into the addons folder. This is located in one of the following locations:
- Windows: `%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\VERSION\scripts\addons`
- Linux: `$HOME/.config/blender/VERSION/scripts/addons`
- MacOS: `/Users/$USER/Library/Application Support/Blender/VERSION/scripts/addons`

**Note**: You will need to replace `VERSION` with your current Blender installation's version.

### Option B: Download and install a Zip archive
Either download from the latest `master` through the `Code` button, or select a release and download the Zip archive there, as shown below.

![](res/images/getting.png)

Select `Edit->Preferences`

![](res/images/installing1.png)

Select `Add-ons->Install` and choose the zip you downloaded. Then enable the plugin by ticking the checkbox next to `Blendgit` as shown below:

![](res/images/installing2.png)

With that out of the way, you can now start using Blendgit!

## Usage

### Files panel
![](res/images/files.png)

- A - File status list
- B - Add single file
- C - Stage all files in list
- D - Reset staged files
- E - Create stash
- F - Pop stash
- G - Commit message
- H - Save commit

### Revisions panel
![](res/images/revisions.png)

- A - Commit log
- B - Load a commit from the list
- C - Switch back to main branch (supports `master` and `main`)
- D - Current branch/commit
- E - Create stash (only visible when there are pending files)
- F - Save commit (only visible when there are pending files)