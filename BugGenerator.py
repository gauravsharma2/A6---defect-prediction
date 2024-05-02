import git
import json
import os
import requests
from bs4 import BeautifulSoup
import re
from pydriller import Repository


class Result():
    def __init__(self, rl, vl) -> None:
        self.version_list = vl
        self.local_repo_link = rl
    def gcl(self,ft,tt):
        r = git.Repo(self.local_repo_link)

        c = []
    
        tag1_obj = r.tags[ft]
        tag2_obj = r.tags[tt]
        for commit in r.iter_commits(rev=f"{tag1_obj}..{tag2_obj}"):
            c.append(commit.hexsha)
        
        return c
    def result(self):
        for i in range(1,len(self.version_list)):
            
            cd = {}

            ft = self.version_list[i-1]
            tt = self.version_list[i]
            
            cl = self.gcl(ft,tt)

            tcf =  0
            tjf = 0
            ujfc = 0
            for c_hash in cl:

                for c in Repository(self.local_repo_link, single=c_hash).traverse_commits():
                    for file in c.modified_files:
                        tcf+=1
                        cn = file.filename
                        if cn.find(".java") != -1:
                            tjf +=1
                            p = r'\bPDFBOX-\d+\b' 
                            bug = re.findall(p, c.msg)
                            cnt = 0
                            for i in bug:
                                if self.cb(i) :
                                    cnt+=1

                            if cn not in cd:
                                ujfc+=1
                                cd[cn] = cnt
                            else:
                                cd[cn]+=1            
          
            fn = f"{ft}-{tt}bug.txt"
            self.scj(fn, cd)

    def cb(self,issueId):
        link = f"https://issues.apache.org/jira/browse/{issueId}"
        res = requests.get(link)
        s = BeautifulSoup(res.text, 'html.parser')
        tv = s.find(id='type-val').get_text()
        return tv.strip() == "Bug"
  
    def scj(self,fileName, data):
        dir = "./BUGS/"
        os.makedirs(dir, exist_ok=True)
        fp = os.path.join(dir, fileName)
        with open(fp, "w") as out: 
            json.dump(data, out)
    


r = Result("/Users/gauravsharma/Desktop/College_Study/Software Maintenance/Assignment_5/pdfbox",['2.0.25','2.0.26','2.0.27','2.0.28','2.0.29','2.0.30','2.0.31'])
r.result()



