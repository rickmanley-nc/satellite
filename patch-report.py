#!/usr/bin/python

import json
import sys
import time

try:
    import requests
except ImportError:
    print "Please install the python-requests module."
    sys.exit(-1)

from argparse import ArgumentParser

import getpass

########################################

def get_json(uname, pword, ssl, location):
    """
    Performs a GET using the passed URL location
    """

    r = requests.get(location, auth=(uname, pword), verify=ssl)

    return r.json()

########################################

def post_json(uname, pword, ssl, location, json_data):
    """
    Performs a POST and passes the data to the URL location
    """

    result = requests.post(
        location,
        data=json_data,
        auth=(uname, pword),
        verify=ssl,
        headers=POST_HEADERS)

    return result.json()

########################################

def pre_write(filed):
  filed.write("<!DOCTYPE html>\n")
  filed.write("<html>\n")

  filed.write("<head>\n")

  filed.write("<style>\n")

  filed.write("table {\n")
  filed.write("    font-family: arial, sans-serif;\n")
  filed.write("    border-collapse: collapse;\n")
  filed.write("    width: 100%;\n")
  filed.write("}\n")

  filed.write("td, th {\n")
  filed.write("    border: 1px solid #dddddd;\n")
  filed.write("    text-align: left;\n")
  filed.write("    padding: 8px;\n")
  filed.write("}\n")

  filed.write("tr:nth-child(even) {\n")
  filed.write("    background-color: #dddddd;\n")
  filed.write("}\n")

  filed.write("</style>\n")

  filed.write("</head>\n")

  filed.write("<body>\n")

  filed.write("<table>\n")

  filed.write("  <tr>\n")
  filed.write("    <th>Organization</th>\n")
  filed.write("    <th>Hostname</th>\n")
  filed.write("    <th>OS</th>\n")
  filed.write("    <th>Environment</th>\n")
  filed.write("    <th>Content View</th>\n")
  filed.write("    <th>All Errata Applied?</th>\n")
  filed.write("    <th>Security Errata</th>\n")
  filed.write("    <th>Bug Fix Errata</th>\n")
  filed.write("    <th>Enhancement</th>\n")
  filed.write("  </tr>\n")

########################################

def post_write(filed):
  filed.write("</table>\n")

  filed.write("</body>\n")

  filed.write("</html>\n")

########################################

def main():
    """
    Main routine that
      - Finds all organizations
      - For each organization
        - Find each host in the organization
        - For each host
          - Print errata information
    """

    # Parse command line arguments

    parser = ArgumentParser()
    parser.add_argument("-s", "--satsvr", dest="satsvr", type=str, default="sat-520a.rhpds.opentlc.com", help="Satellite server to query")
    parser.add_argument("-u", "--user", dest="USERNAME", type=str, help="User name")
    parser.add_argument("-p", "--password", dest="PASSWORD", type=str, help="Password")
    parser.add_argument("--ssl", dest="SSL_VERIFY", default="False", type=str, help="Observe SSL errors - True or (default) False")
    parser.add_argument("-l", "--logdir", dest="LOGDIR", type=str, help="Log directory")
    args = parser.parse_args()

    # Prompt for username if needed

    if not args.USERNAME:
      username = raw_input("Username:  ")
    else:
      username = args.USERNAME

    # Prompt for password if needed

    if not args.PASSWORD:
      password = getpass.getpass()
    else:
      password = args.PASSWORD

    # Define SSL variable

    if args.SSL_VERIFY == "False":
      ssl_ver = False
    else:
      ssl_ver = True

    # Define the output file (if not specified, use stdout)

    if args.LOGDIR:
      logdir = args.LOGDIR
      filename = logdir + "/" + time.strftime("%m-%d-%Y") + "-patchreport.html"
      fileo = open(filename, 'w')
    else:
      fileo = sys.stdout

    # Compose the URL to the Satellite 6 server

    URL = "https://" + args.satsvr + "/"

    # URL for the API to the Satellite 6 server

    #SAT_API = "%s/katello/api/v2/" % URL
    SAT_API = "%s/api/" % URL

    # Katello-specific API

    KATELLO_API = "%s/katello/api/" % URL
    POST_HEADERS = {'content-type': 'application/json'}

    # Write out the initial part of the HTML file

    pre_write(fileo)

    # Get the list of Organizations
    # API:  /katello/api/organizations

    orgs = get_json(username, password, ssl_ver, KATELLO_API + "organizations/")

    for i_org in orgs['results']:

      # Get a list of hosts in the organization
      # API:  /api/hosts - this lists all hosts
      # API:  /api/organizations/:organization_id/hosts

      orghosts = get_json(username, password, ssl_ver, SAT_API + "organizations/" + str(i_org['id']) + "/hosts")

      for i_orghost in orghosts['results']:
        security_errata = i_orghost['content_facet_attributes']['errata_counts']['security']
        bugfix_errata = i_orghost['content_facet_attributes']['errata_counts']['bugfix']
        enhancement_errata = i_orghost['content_facet_attributes']['errata_counts']['enhancement']

        if (security_errata + bugfix_errata + enhancement_errata) > 0:
          all_patches_applied = "No"
        else:
          all_patches_applied = "Yes"

        fileo.write("  <tr>\n")
        fileo.write("    <td>{}</td>\n".format(i_org['name']) )
        fileo.write("    <td>{}</td>\n".format(i_orghost['name']) )
        fileo.write("    <td>{}</td>\n".format(i_orghost['operatingsystem_name']) )
        fileo.write("    <td>{}</td>\n".format(i_orghost['content_facet_attributes']['lifecycle_environment_name']) )
        fileo.write("    <td>{}</td>\n".format(i_orghost['content_facet_attributes']['content_view_name']) )
        fileo.write("    <td>{}</td>\n".format(all_patches_applied) )
        fileo.write("    <td>{}</td>\n".format(str(security_errata)) )
        fileo.write("    <td>{}</td>\n".format(str(bugfix_errata)) )
        fileo.write("    <td>{}</td>\n".format(str(enhancement_errata)) )
        fileo.write("  </tr>\n")

#        print "Organization       :  " + i_org['name']
#        print "Hostname           :  " + i_orghost['name']
#        print "OS                 :  " + i_orghost['operatingsystem_name']
#        print "Environment        :  " + i_orghost['content_facet_attributes']['lifecycle_environment_name']
#        print "Content View       :  " + i_orghost['content_facet_attributes']['content_view_name']
#        print "All Errata Applied?:  " + all_patches_applied
#        print "Security Errata    :  " + str(security_errata)
#        print "Bug Fix Errata     :  " + str(bugfix_errata)
#        print "Enhancement        :  " + str(enhancement_errata)
#        print ""

    # Write out the final part of the HTML file

    post_write(fileo)

    # Close the file

    fileo.close()

    # Get a list of errata

#    errata = get_json(username, password, ssl_ver, KATELLO_API + "errata/")
#    print errata

########################################

if __name__ == "__main__":
    main()
