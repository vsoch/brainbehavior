import praw
import pickle
import sys


disorder = sys.argv[1]
outfolder = sys.argv[2]

r = praw.Reddit(user_agent='cogatpheno')

print "Parsing %s" %disorder
submissions = r.get_subreddit(disorder).get_hot(limit=1000)
now = time.localtime()
content = []
ids = []
scores = []
for sub in submissions:
        if len(sub.selftext) > 0:
            content.append(sub.selftext)
            ids.append(sub.fullname)
            scores.append(sub.score)
            if sub.num_comments > 0:
                comments = sub.comments
                while len(comments) > 0:
                    for comment in comments:
                        current = comments.pop(0)
                        if isinstance(current,praw.objects.MoreComments):
                            comments = comments + current.comments()
                        else:               
                            if len(current.body)>0:     
                                content.append(current.body)
                                ids.append(current.fullname)
                                scores.append(current.score)

print "%s has %s entities" %(disorder,len(content))
result = {"content":content,"disorder":disorder,"score":scores,"uids":ids,"retrieved":now}
pickle.dump(result,open("%s/%s_dict.pkl" %(outfolder,disorder),"wb"))
