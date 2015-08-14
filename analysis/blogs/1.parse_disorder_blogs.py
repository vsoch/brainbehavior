# Let's try to parse the blog content

from brainbehavior.browser import get_browser, run_javascript, get_page
from random import randint
from time import sleep
import pickle
import numpy

browser = get_browser()
blogdict = pickle.load(open("/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/blogs/disorder_blogs.pkl","rb"))

# Function to get blogger entries
entryfn = '''
entries = document.getElementsByClassName("entry-title")
var pages = [];
for (i = 0; i < entries.length; i++) { 
    pages.push(entries[i].children[0].href)
}
return pages
'''



allblogpages = dict()

# Load the blog URLS
for disorder,blogs in blogdict.iteritems():
    print "Parsing disorder blogs: %s" %(disorder)
    unique_blogs = numpy.unique(blogs).tolist()
    blogpages = dict()
    for b in range(0,len(unique_blogs)):
        print "%s of %s" %(b,len(unique_blogs))
        blog = unique_blogs[b]
        browser.get("http://%s" %blog)
        # For now just get most recent pages
        try:
            blogpages[blog] = run_javascript(browser,entryfn)
        except:
            print "Error with %s"
    allblogpages[disorder] = blogpages

# We want each one to go to a different node so there are different IP addresses and times
pickle.dump(allblogpages,open("/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/blogs/disorder_blog_pages.pkl","wb"))
