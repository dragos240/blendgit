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

### Versions panel
You may create new commits or load previous ones in this panel.

![](res/images/versions-panel.png)

#### Saving new commits
- Enter a commit message and click `Save Commit`.
- You may enable the `Also restore stash` option if you have a previous stash you wish to restore before you commit.

#### Loading old commits
- Select a previous commit from the drop-down menu and click `Load Commit`..
- You can choose to stash your current uncommitted work with the `Stash before load` option.

### Branches panel
You may switch to an existing branch or create a new one in this panel.

![](res/images/branches-panel.png)

#### Switching branches
- You may switch to an existing branch by selecting the name of the branch from the drop-down menu and clicking `Switch Branch`.
- You can choose to stash your current uncommitted work with the `Stash before load` option.

#### Creating branches
- Enter a valid name for a new branch and click `Create Branch`.