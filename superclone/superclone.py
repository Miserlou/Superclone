#! /usr/bin/env python

import requests
import argparse
import sarge
from BeautifulSoup import BeautifulSoup

MERCURIAL = 'hg'
GIT = 'git'
CVS = 'cvs'
SUBVERSION = 'svn'

HGWEB_IDENT = '<table class="bigtable">'

def superclone(args):

    # Get page content
    # Extract list of repos
    # Start workers 
        # Clone threads

    url = args['url'][0]
    web_response = requests.get(url)

    if web_response.status_code != 200:
        raise Exception

    page_content = web_response.content
    repos, repo_type = extract_repos(page_content)

    for repo in repos:
        clone_repo(url + repo, repo_type)

    print "Done!"

    return

def extract_repos(html_content):

    scraper_type = None

    # Mercurial
    if HGWEB_IDENT in html_content:
        scraper_type = MERCURIAL
        repos = extract_mercurial(html_content)

    # elif git:
    #   craper_type = GIT
    # etc

    else:
        raise Exception("Content at given URL is not supported.")


    return repos, scraper_type

def extract_mercurial(html_content):

    soup = BeautifulSoup(html_content)
    table = soup.find('table')

    if not table:
        raise Exception("Misclassification.")

    repos = []
    for row in table.findAll('tr')[1:]:
        link = row.findAll('a')[0]['href']
        repos.append(link)

    return repos

def clone_repo(address, repo_type):

    if repo_type == MERCURIAL:
        print MERCURIAL, 'clone', address


    else:
        raise Exception(repo_type, "is not yet supported.")        


def get_parser():
    parser = argparse.ArgumentParser(description='SuperClone. Give it a GitWeb or HGWeb index url, and it\'ll rapidly snarf everything.')
    parser.add_argument('url', metavar='URL', type=str, nargs='*',
            help='the url of the server to scrape.')
    parser.add_argument('-t','--threads', help='Number of threads to use', default=10, dest='threads', type=int)
    return parser

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    if not args['url']:
        parser.print_help()
        return
    else:
        try:
            superclone(args)
        except (KeyboardInterrupt, SystemExit):
            print "" 
            quit()
        except Exception, e:
            print "Something went wrong!"
            print e
            quit()

if __name__ == '__main__':
    try:
        command_line_runner()
    except (KeyboardInterrupt, SystemExit):
        print "" 
        quit()
    except Exception, e:
        quit()