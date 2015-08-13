# We will try scraping blog content with python splash
#
# First need to start splash server
# python -m splash.server --max-timeout 120

from brainbehavior.browser import get_browser, get_page, get_blogs, next_page
import pickle

# Set up a web browser
browser = get_browser()
get_page(browser,"http://www.searchblogspot.com")
search_parent = browser.find_element_by_class_name('gsc-search-button')
search_box = search_parent.find_elements_by_css_selector("*")

# Read in list of disorders to search for
disorders = ["depression","anxiety","stress","OCD","panic","phobia","PTSD",
             "anorexia","bulimia","autism","amnesia","Alzheimer's","bipolar disorder",
             "schizophrenia","narcissism","narcolepsy","drug abuse"]

# We will store urls in a dictionary
blogdict = dict()

for disorder in disorders:

    # Get the total number of results
    number_pages = browser.execute_script('''
        var search_box = arguments[0];
        var value = arguments[1];
        document.getElementsByClassName("gsc-input")[0].children[0].value= value;
        document.getElementsByClassName("gsc-search-button")[0].children[0].click();
        return document.getElementsByClassName("gsc-cursor")[0].lastChild.textContent
    ''', search_box, disorder)

    # Get the blog results on the first page
    urls = []
    urls = urls + get_blogs(browser)

    # For each following page, push buttons and get new blogs
    for i in range(1,int(number_pages)-1):
        next_page(browser,i)
        urls = urls + get_blogs(browser)

    blogdict[disorder] = urls

pickle.dump(blogdict,open("/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/blogs/disorder_blogs.pkl","wb"))
