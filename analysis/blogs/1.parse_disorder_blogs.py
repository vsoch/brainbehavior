# Let's try to parse the blog content

from brainbehavior.browser import get_browser, run_javascript
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

# Function to get content
contentfn = '''
return document.getElementsByClassName("entry-content")[0].children[0].textContent
'''


allblogcontent = dict()

# Load the blog URLS
for disorder,blogs in blogdict.iteritems():
    unique_blogs = numpy.unique(blogs).tolist()
    blogcontent = dict()
    for blog in unique_blogs:
        content = []
        get_page(browser,blog)
        # For now just get content from most recent pages
        pages = run_javascript(browser,entryfn)
        for page in pages:
            get_page(browser,page)
            content.append(run_javascript(browser,contentfn))
        blogcontent[blog] = content
    allblogcontent[disorder] = blogcontent

pickle.dump(blogdict,open("/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/blogs/disorder_blog_content.pkl","wb"))

