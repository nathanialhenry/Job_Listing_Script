# Job_Listing_Script
This script sends an email if there are any new job postings listed on the EA Careers website in a desired position.
It saves search results and compares new results to it so that you don't get redundant information in your email.

Need to install Selenium and Chromedriver (in the Requirements.txt) to run. Will also need command line arguments for: (--path "chromedriver path", --user "username for sending emails", --password "password for email account", --to "recipient email", --job "type of job being searched (can be multiple, see help option when running script).

It is best used with cron job or task scheduler and with a batch file for command line arguments.

-Note: This script will create multiple .txt files

