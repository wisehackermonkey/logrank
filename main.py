# process pages into just links
import re
import pprint
import glob
import os
import collections
# pip install networkx[default,extra]
import networkx as nx

def extract_link_names(input_text):
    link_name_pattern=r"\[\[(.*?)\]\]" # regexr.com/75ord

    # input_text=""""
    # tag [[hardware]] [[software]] [[circuit]] [[launch]] [[homebrew]]  robotics club  nyc hardware startup meeting
    # Circuitlaunch circuit launch
    # """
    results = re.findall(link_name_pattern,input_text)
    # pprint.pprint("found: "+str(len(results)))
    return dict.fromkeys(results)
def sortbyrank(e):
    return e[1]
if __name__ == "__main__":
    #extract all links for each page into list of links
    # read all files names into list
    file = "/mnt/c/Users/o/github/notes_v1/pages/*.md"
    all_pages = glob.glob(file)#"C:/Users/o/github/notes_v1/pages/*.md")
    db = []
    for page in all_pages:
        with open(page,"r",encoding="utf-8") as f:
            page_name = os.path.basename(page)[:-3]
            file_text = f.read()
            links = extract_link_names(file_text)
            
            links = list(sorted(set(links)))
            # print(f"'{page_name}':{links}",)
            print(".",end=" ")
            db += [[page_name,links]]
    
    # make list of all links
    all_links = [x[1] for x in db]
    all_links = [item for sublist in all_links for item in sublist]
    
    
    # convert the links db into the following form
    # from name, [links] to [(name,link),(name,link)....]
    # pprint.pprint(db[1:10])
    D= nx.DiGraph()
    counter = 0 
    
            
    print(counter)
    connections_db = []
    for page in db:
        page_name = page[0]
        links = page[1]
        results = []
        for link in links:
            counter +=1
            connections_db += [[page_name,link]] 
    # pprint.pprint(connections_db[:-10])
     
    connections_db = [x+[counter/100] for x in connections_db]
    D.add_weighted_edges_from(connections_db)

    page_ranked_raw =nx.pagerank(D)
    # print(page_ranked_raw)
    page_ranked_clean = page_ranked_raw.items()
    most_valuable_pages = sorted([[x[1],x[0]] for x in list(page_ranked_clean)])
    [ print(f"rank: {x[0]},{x[1]}") for x in most_valuable_pages[-100:]]
