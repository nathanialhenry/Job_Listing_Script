# TODO find object best for comparison of the two sets of Listings and format the email better

from selenium import webdriver
import os, argparse, smtplib, json, re

# TODO improve email formatting
# create command line argumets for sensitive/desired information
parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, default="/usr/bin/chromedriver", help="Insert Filepath for selenium web driver (chromedriver, gecko, etc)" )
parser.add_argument("--user", type=str, help="Username to send emails with" )
parser.add_argument("--password", type=str, help="Password of Username" )
parser.add_argument("--to", type=str, help="Username to send emails to" )
parser.add_argument("--job", type = str, action = 'append', help="type job being searched (i.e. 'Sr Quality Analyst'), can search multiple positions by calling the argument multiple times (i.e. --job 'Producer' --job 'Artist')" )
args = parser.parse_args()

# create gmail function to call when sending an email
def send_email(text):
    gmail_user = args.user
    gmail_password = args.password
    sent_from = gmail_user
    to = args.to
    subject = 'New Job Listings from EA'
    body = encoded_text
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, to, subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print ('Email sent!')
    except Exception as e:
        print("An exception has occurred at {0}".format(e))

# Expands a "#shadow-root" element
def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

# load and use the driver to get url and create a wait time for class element in DOM
driver = webdriver.Chrome(args.path)
driver.get("https://www.ea.com/careers/careers-overview/vancouver#roles")

# Fetch the #shadow-root parent and use that to expand
root_element = driver.find_element_by_tag_name("eacom-jobs-list")
shadow_element = expand_shadow_element(root_element)

# access element with appropriate children
job_table = shadow_element.find_element_by_class_name('eacom-jobs-list__table')

# access table row with job information
jobListing = job_table.find_elements_by_class_name('eacom-jobs-list__row')

# declare jobs of interest and variables to store results
JOBS_OF_INTEREST = args.job

results_dict = {}
key_counter = 0
# Loop through listings from the web element and create dicts/lists
for listing in jobListing:
  for job in JOBS_OF_INTEREST:
    if (job in listing.text):
        results_dict ['url {0}'.format([key_counter])] = (listing.get_attribute("href"))
        results_dict ['job{0}'.format([key_counter])] = (listing.text.split("\n")[0])
        key_counter += 1

# creates jobFile.txt if it doesn't already exist
emptyJson = 'Empty'
file_check = os.path.isfile('jobFile.json')
if file_check == False:
    with open('jobFile.json', 'w') as f:
        f.dump(emptyJson)
    f.close()

# open previously saved results from JSON and append them to older_results variable for comparison
older_results_dict = {}
try:
    with open('jobFile.json', 'r') as json_file:
        older_results_dict = json.load(json_file)
        older_results_list = older_results_dict
    json_file.close()
except Exception as e:
    print("There has been an Exception at %s" % (e))

# creates a variable containing the difference of the new listings - the old listings
difference_of_dicts = {key : results_dict[key] for key in set(results_dict) - set(older_results_dict)}

# format email text (i.e. Job : Url /n))  
sorted_results = []


for key in sorted(difference_of_dicts.keys()):
    sorted_results.append(difference_of_dicts[key])


print("these results were found to be recent additions to the ea site:{0}".format(sorted_results))

# update the jobFile.txt document with most up to date job listings
with open('jobFile.json', 'w') as file:
    json.dump(results_dict, file, indent = 2)
file.close()

# send email with new listings if there was any changes between older scrapes and newer scrapes
if sorted_results:

    formated_email = ""
    counter = 0
    len_sorted_results = len(sorted_results)
    url_half = (int(len_sorted_results/2))

    while counter < url_half:
        formated_email += sorted_results[counter] + " : " + sorted_results[(counter+ url_half)] + " \n "
        counter +=1

    #  .encode('ascii', 'ignore')

    print("sending email...")
    text = ("Hello, \n \n These are the new job listings found on the EA Vancouver Careers website: \n \n %s" %(formated_email))
    encoded_text = text
    send_email(encoded_text)
else:
    print("No new listings to report")

# close webdriver
driver.quit()
