
# Digi Ghosting

Digi Ghosting is a multi-dimensional program that allows users to delete their digital identity/footprint from popular social media applications. Digi Ghosting allows users to input their email and delete the social media accounts tied to that email. Digi Ghosting supports a GUI for GMAIL based accounts and an external program/script for other email accounts. The relevant instructions can be found under Method 1 for GMAIL users and Method 2 for all other emails on how to set up and run the program.


## Authors

- [@Rxelxius](https://github.com/Rxelxius)
- [@xllRyan](https://github.com/xllRyan)
- [@Bransontian](https://github.com/Bransontian)
- [@nemoislost-cmd](https://github.com/nemoislost-cmd)


## Requirements / Pre Requisite
- Ensure that Google Chrome is updated to it's latest version
- Ensure that 2FA is not enabled for any of the social media accounts that are about to be deleted
- For Gmail users, extraction of credentials will be done from Google Password Manager so ensure that credentials for all relevant social media accounts are stored there.

## Installation and Usage  (Method 1)


Download the project file as a zip file from GitHub and unzip it 

Go to the project directory where the unzipped files are located

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Move the folder called webdrivers into your C: drive 

```bash
  xcopy webdrivers c:\
```


Navigate to project directory and run main.py

```bash
  python main.py
  
```

## Installation and Usage (Method 2) 

- Download Uipath Studio from https://www.uipath.com
- Download the automation process file "ICT2202_DigiGhosting_Ui" from Github
- Open UiPath Studio and run the 'project' JSON located in "ICT2202_DigiGhosting_Ui"
- Click on "Debug File" dropdown bar followed by "Run File"
- Follow the instruction shown in the pop up.
## Support

For support, email 
- 2102536@sit.singaporetech.edu.sg 



## Demo











