import web_scraper
import sys

def is_link_in_page(page_to_check, end_link):
    links_on_page = web_scraper.getAllUrl(page_to_check)
    if end_link in links_on_page:
        return True
    else:
        return False

#get all links for n degree higher
def get_all_degree_links(degree, start_degree_pages, end_link, path, reverse_path_last_degree):
    current_degree_pages = set()
    #if no more degrees to go return all links of current degree
    if degree == 0:
        return start_degree_pages
    #for each page in current degree get all URLS
    for page in start_degree_pages:
        all_pages = web_scraper.getAllUrl(page)

        #remove all duplicate pages that we already checked
        for degrees in path:
            all_pages.difference_update(degrees)

        current_degree_pages = current_degree_pages.union(all_pages)

        #if end link found return
        if end_link in all_pages:
            print("Found the Page in get_all_degree_links")
            return current_degree_pages.union(all_pages)

        #check for overlap
        overlap = all_pages & reverse_path_last_degree
        if len(overlap) > 0:
            print("Found a Overlap")
            print(overlap)
            return current_degree_pages.union(all_pages)

    
    return get_all_degree_links(degree - 1, current_degree_pages, end_link, path, reverse_path_last_degree)


def get_all_reverse_degree_links(degree, start_degree_pages, start_link, path, end_link):
    current_degree_pages = set()
    #if no more degrees to go return all links of current degree
    if degree == 0:
        return start_degree_pages
    #for each page in current degree get all URLS
    for page in start_degree_pages:
        
        all_pages = web_scraper.getAllBackLinks(page)

        #remove all duplicate pages that we already checked
        for degrees in path:
            all_pages.difference_update(degrees)


        current_degree_pages = current_degree_pages.union(all_pages)

        #if end link found return
        if end_link in all_pages:
            print("Found the Page in reverse Degree")
            return current_degree_pages.union(all_pages)

    #do same for next degree
    return get_all_reverse_degree_links(degree - 1, current_degree_pages, start_link, path, end_link)


#set the start and end wiki page title
# start_link = "Pretoria".lower()
# end_link = "frankenstein".lower()

# end_link = "Sovereign_state"
#this is the path to start with


def degree_distance(start_link, end_link):
    path = [{start_link.lower()}]
    reverse_path = [{end_link.lower()}]

    #check if they are 0 degrees away
    # if start_link == end_link:
    #     print("They are the same")
    #     sys.exit()

    #start with 1 degree
    degree_count = 1


    while degree_count < 12:
        print("Calling path")
        # print(f"calling function with: path: {path[degree_count - 1]} and {end_link}")
        path.append(get_all_degree_links(1, path[degree_count - 1], end_link, path, reverse_path[-1]))

        #check if link in that degree
        # print(path)
        if end_link in path[degree_count]:
            print("One Direction")
            print("They are {} clicks away".format(degree_count))
            return degree_count

        overlap = path[-1] & reverse_path[-1]
        print(overlap)
        if len(overlap) > 0:
            print("Both Directions")
            print(overlap)
            # print(path)
            print("They are {} clicks away".format(len(path) + len(reverse_path) - 2))
            return (len(path) + len(reverse_path) - 2)

        # print(path)
        print("Calling reverse_path")
        reverse_path.append(get_all_reverse_degree_links(1, reverse_path[degree_count - 1], start_link, reverse_path, start_link))
        # print(reverse_path)
        degree_count += 1

        overlap = set(path[degree_count - 1]) & set(reverse_path[degree_count - 1])
        if len(overlap) > 0:
            print("Both Directions")
            print(overlap)
            # print(path)
            print("They are {} clicks away".format(len(path) + len(reverse_path) - 2))
            return (len(path) + len(reverse_path) - 2)




#Search until the end link is found

#get all links of one degree higher
#path.append(get_all_degree_links(1, path[degree_count - 1]))
# #check if link in that degree
# if end_link in path[degree_count]:
#     print("They are {} clicks away".format(degree_count))

# reverse_path.append(get_all_reverse_degree_links(1, reverse_path[degree_count - 1]))
# degree_count += 1


# overlap = set(path[degree_count - 1]) & set(reverse_path[degree_count - 1])
# print(path[degree_count - 1])
# print(reverse_path[degree_count - 1])
# if len(overlap) > 0:
#     print("They are {} clicks away".format(len(path) + len(reverse_path) - 2))