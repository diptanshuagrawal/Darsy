# Dutchman

###INSTALLATION

The application runs only on localhost. You will need a local server to run it. Here are steps on how to do it.

1. Install XAMPP Server (With PHP 7+ version), It is available for Linux, Windows and Mac.

2. You will need to change the configuration of the server.
    1. Change the DocumentRoot to the address of this project.
    2. Change the cgi-bin address to the same address as above.
    3. To Allow Cross Origin Resource sharing (A necessity in localhost), you will need to add a line

              ```
                <Directory />
                    Header set Access-Control-Allow-Origin "*"
                    ***some other statements***
                </Directory>
              ```
            
3. These scripts right now do not create any database table, it is assumed they are already present. You may need to add all the
    tables yourself.

4. You will have to install all the required modules for running the python scripts, which do not come with XAMPP. Some of them
    include MySQLdb, wikipedia. Please make sure all the packages are installed with python3+ support. One
    of the easiest way to do that is use pip3 (it is different from the pip module available for the python2x version).
5. You will also need to give execution permission to all the python scripts. You can do that by running  either

		```
			chmod +x *
		```
	or
		```
			chmod 755 *
		```
	in the root/python directory

### USAGE

Open index.html in Chrome as Speech to Text will only work in chrome.
# Darsy
