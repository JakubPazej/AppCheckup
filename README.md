# AppCheckup QuickStart Guide
1.  #### Install Java
+	Is at least Java 1.8 installed?
+	Does executing `java -version` on command line/command prompt return 1.8 or greater?
+	If not, please install Java 8+ and make it the default.
2.  #### Install APKTool
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Note - You can also decompile an `.apk` manually by renaming the file name extension from `.apk` to `.rar` and extracting it.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Note - Wrapper scripts are not needed, but helpful so you do not have to type `java -jar apktool.jar` over and over.
+   Windows 
    *	Download Windows [wrapper script](https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat) (Right click, Save Link As apktool.bat)
    *	Download apktool-2 ([find newest here](https://bitbucket.org/iBotPeaches/apktool/downloads/))
    *	Rename downloaded jar to `apktool.jar`
    *	Move both files (`apktool.jar` & `apktool.bat`) to your Windows directory (`Usually C://Windows`)
    *	If you do not have access to `C://Windows`, you may place the two files anywhere then add that directory to your Environment Variables System PATH variable.
    *	Try running `apktool` via command prompt
+   Linux
    *	Download Linux [wrapper script](https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool) (Right click, Save Link As apktool)
    *	Download apktool-2 ([find newest here](https://bitbucket.org/iBotPeaches/apktool/downloads/))
    *	Rename downloaded jar to `apktool.jar`
    *	Move both files (`apktool.jar` & `apktool`) to `/usr/local/bin` (root needed)
    *	Make sure both files are executable (`chmod +x`)
    *	Try running `apktool` via cli
+   macOS 
    *	Download Mac [wrapper script](https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/osx/apktool) (Right click, Save Link As apktool)
    *	Download apktool-2 ([find newest here](https://bitbucket.org/iBotPeaches/apktool/downloads/))
    *	Rename downloaded jar to `apktool.jar`
    *	Move both files (`apktool.jar` & `apktool`) to `/usr/local/bin` (root needed)
    *	Make sure both files are executable (`chmod +x`)
    *	Try running `apktool` via cli
 
Or you can install apktool via Homebrew:
+	Install Homebrew as described [in this page](https://brew.sh/)
+	Execute command `brew install apktool` in terminal (no root needed). The latest version will be installed in `/usr/local/Cellar/apktool/[version]/` and linked to `/usr/local/bin/apktool`.
+	Try running `apktool` via cli
3.  #### Install Python
+	Is at least python 3.9 installed?
+	Does executing `python --version` on command line/command prompt return 3.9 or greater?
+	If not, please install Python 3.9+ and make it the default.
4.  #### Clone the repository
+	Open the command line/command prompt and navigate to the folder where you wish to download the project scripts
+	Execute `git clone https://github.com/JakubPazej/AppCheckup`
5.  #### Install the requirements.txt
+	Open the command line/command prompt and navigate into the project folder
+	Execute `pip install -r requirements.txt`
6.  #### Run download.py
+	Find an app you want to download on the google play market
+	Copy the link after the ‘=’ sign at the end for example: `https://play.google.com/store/apps/details?id=com.whatsapp` you would copy `com.whatsapp`
+	Open the command line/command prompt and navigate into the project folder
+	Execute the download script with your copied link as an argument: `python download.py com.whatsapp`
7.  #### Run APKTool
+	Open the command line/command prompt and navigate into the output folder inside the project folder
+	Execute `apktool d <APK_NAME>` i.e.: `apktool d whatsapp.apk`
+	APKTool is now going to extract the apk into its pre-compile files, this process can take up to one minute or more. Make sure the AndroidManifest.xml got properly extracted into the folder named after the app.
8.  #### Run permissions.py
+	Open the command line/command prompt and navigate into the output folder inside the project folder
+	Execute `python permissions.py <APK_FOLDER>` i.e.: `python permissions.py whatsapp`
+	Examine what permissions the tested app requires from its AnrdoidManifest.xml through the information printed out by the script


