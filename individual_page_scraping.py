# Scraping a LIST.AM post page from file

import os
import requests
import bs4
from datetime import datetime
import time
import re
import sqlite3

# define unitility fields: current date and time, bad characters
now = datetime.now()
timestamp0 = datetime.timestamp(now)
timestamp = datetime.fromtimestamp(timestamp0).isoformat()

# Manually set the run date/time
##manual_date="2021/07/12 21:00:35"
##now = datetime.strptime(manual_date, "%Y/%m/%d %H:%M:%S")
##timestamp0 = time.mktime(datetime.strptime(manual_date, "%Y/%m/%d %H:%M:%S" ).timetuple())
####print("Timestamp0 ", timestamp0)
##timestamp = datetime.fromtimestamp(timestamp0).isoformat()
####print("timestamp ", timestamp)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
counter = 0
start = time.perf_counter()  # return the value (in fractional seconds) of a performance counter, i.e. a clock with teh highest available resolution to measure a short duration. It does include time elapsed during sleep and is system-wide. The reference point of the returned value is undefined, so that the difference between the results of two calls is valid.

# Connect to databases

connection_LISTAM_Active = sqlite3.connect("D:\Database\LISTAM_Active.db")
cursor_LISTAM_Active = connection_LISTAM_Active.cursor()

# Retrieve Content from the database

post_content_list = cursor_LISTAM_Active.execute("select PostListWContent.Post_ID, PostListWContent.Post_Content \
                                                from PostListWContent \
                                                where PostListWContent.Post_ID >0 \
                                                order by PostListWContent.Post_ID")

##post_content_list = cursor_LISTAM_Active.execute("select PostListWContent.Post_ID, PostListWContent.Post_Content \
##                                                from PostListWContent \
##                                                where PostListWContent.Post_ID not in (select Posts_Active.PostReferenceNumber from Posts_Active) \
##                                                AND PostListWContent.Post_ID not in (select Posts_Deleted.PostReferenceNumber from Posts_Deleted) \
##                                                order by PostListWContent.Post_ID ASC")

list_of_posts = []
for row in post_content_list:
    list_of_posts.append(row)

total_number = len(list_of_posts)
# print(total_number)
# print("post id: ", list_of_posts[0][0])
# print("post content: ", list_of_posts[0][1])


for i in list_of_posts[:]:
    ##        file_location=i.split(",")[0]
    ##        file_name=i.split(",")[1]
    ##        post_id_from_name=file_name.split("_")[2]
    ##        #print(post_id_from_name, ": ", file_location, " - ", file_name)
    post_id_from_name = i[0]
    print("started to process post id: ", post_id_from_name)
    post_list = []
    ##        #file_location = "E:\Training\PythonTraining\Training Code\LISTAM_output\Post_outputs\LISTAM_real estate_9121076_HTML_Parser_1621144167.429521.html"
    ##
    ##        # open file from the hard drive
    ##        with open(file_location,"r",encoding="UTF-8") as html_f:
    ##            soup = bs4.BeautifulSoup(html_f, "html.parser")   #"html.parser", 'lxml'
    ##        #print(soup.prettify())

    # read content from the database
    soup = bs4.BeautifulSoup(i[1], "html.parser")
    # print(soup.prettify())

    ##Extract values from the webpage

    # tblPost_Field1 - ProgramRunTimestamp
    post_list.append(timestamp)
    # tblPost_Field2 - RecordCreateTimestamp
    post_timestamp = datetime.fromtimestamp(datetime.timestamp(now)).isoformat()
    post_list.append(post_timestamp)
    # tblPost_Field3 - PostReferenceNumber
    post_reference = post_id_from_name
    post_list.append(post_reference)
    # tblPost_Field4,5,6,7,8,9,10,11 - Categories
    findSectionCrumbs = soup.find_all("li")
    number_SectionCrumbs = len(findSectionCrumbs)
    # print(number_SectionCrumbs)
    try:
        Category1 = findSectionCrumbs[0].text.lstrip().rstrip()
    except:
        Category1 = None
    post_list.append(Category1)

    try:
        Category2 = findSectionCrumbs[1].text.lstrip().rstrip()
    except:
        Category2 = None
    post_list.append(Category2)

    try:
        Category3 = findSectionCrumbs[2].text.lstrip().rstrip()
    except:
        Category3 = None
    post_list.append(Category3)

    try:
        Category4 = findSectionCrumbs[3].text.lstrip().rstrip()
    except:
        Category4 = None
    post_list.append(Category4)

    try:
        Category5 = findSectionCrumbs[4].text.lstrip().rstrip()
    except:
        Category5 = None
    post_list.append(Category5)

    try:
        Category6 = findSectionCrumbs[5].text.lstrip().rstrip()
    except:
        Category6 = None
    post_list.append(Category6)

    try:
        Category7 = findSectionCrumbs[6].text.lstrip().rstrip()
    except:
        Category7 = None
    post_list.append(Category7)

    Category8 = []
    try:
        for i in findSectionCrumbs[7:]:
            Category8_row = i.text.lstrip().rstrip()
            Category8.append(Category8_row)
    except:
        pass
    if Category8 == []:
        Category8a = None
        post_list.append(Category8a)
    else:
        Category8b = "#".join(map(str, Category8))
        post_list.append(Category8b)

    findSectionPContent = soup.find("div", id="pcontent")

    if findSectionPContent == None:
        deleted_posts = []
        deleted_posts.append(timestamp)
        deleted_posts.append(post_timestamp)
        deleted_posts.append(post_reference)
        cursor_LISTAM_Active.execute("Insert INTO Posts_Deleted VALUES (?,?,?)", deleted_posts)
        connection_LISTAM_Active.commit()
        counter = counter + 1
        print(str(total_number), "/", str(counter), "--added to the Posts_Deleted table: ", post_reference)
        continue
    else:
        pass

    # tblPost_Field 12 - Title
    try:
        Title = findSectionPContent.find("h1").text.lstrip().rstrip()

    except:
        Title = None
    post_list.append(Title)

    # tblPost_Field 13 - Price
    if findSectionPContent.find("span", class_="price") is None:
        Price = None
    else:
        Price = findSectionPContent.find("span", class_="price").text.lstrip().rstrip()
    post_list.append(Price)
    # tblPost_Field 14,15,16 - Locations
    if findSectionPContent.find(class_="loc") is None:
        Location1 = None
        post_list.append(Location1)
        Location2 = None
        post_list.append(Location2)
        Location3 = None
        post_list.append(Location3)
    else:
        num_locations = (findSectionPContent.find(class_="loc").text.split("›"))
        try:
            Location1 = num_locations[0].lstrip().rstrip()
        except:
            Location1 = None
        post_list.append(Location1)

        try:
            Location2 = num_locations[1].lstrip().rstrip()
        except:
            Location2 = None
        post_list.append(Location2)

        Location3 = []
        try:
            for i in num_locations[2:]:
                Location3_row = i.text.lstrip().rstrip()
                Location3.append(Location3_row)
        except IndexError:
            pass

        if Location3 == []:
            Location3a = None
            post_list.append(Location3a)
        else:
            Location3b = "#".join(map(str, Location3))
            post_list.append(Location3b)
            # tblPost_Field 17,18 - cLabels
    clabels = (findSectionPContent.find_all(class_="clabel"))
    if clabels == []:
        cLabel_1 = None
        post_list.append(cLabel_1)
        cLabel_2 = None
        post_list.append(cLabel_2)
    else:
        try:
            cLabel_1 = clabels[0].text.lstrip().rstrip()
        except:
            cLabel_1 = None
        post_list.append(cLabel_1)

        cLabel_2 = []
        try:
            for i in clabels[1:]:
                cLabel_2_row = i.text.lstrip().rstrip()
                cLabel_2.append(cLabel_2_row)
        except IndexError:
            pass

        if cLabel_2 == []:
            cLabel_2a = None
            post_list.append(cLabel_2a)
        else:
            cLabel_2b = "#".join(map(str, cLabel_2))
            post_list.append(cLabel_2b)
            # tblPost_Field 19,20 - uLabels
    ulabels = (findSectionPContent.find_all(class_="ulabel"))
    if ulabels == []:
        uLabel_1 = None
        post_list.append(uLabel_1)
        uLabel_2 = None
        post_list.append(uLabel_2)
    else:
        try:
            uLabel_1 = ulabels[0].text.lstrip().rstrip()
        except:
            uLabel_1 = None
        post_list.append(uLabel_1)

        uLabel_2 = []
        try:
            for i in ulabels[1:]:
                uLabel_2_row = i.text.lstrip().rstrip()
                uLabel_2.append(uLabel_2_row)
        except IndexError:
            pass

        if uLabel_2 == []:
            uLabel_2a = None
            post_list.append(uLabel_2a)
        else:
            uLabel_2b = "#".join(map(str, uLabel_2))
            post_list.append(uLabel_2)

            # tblPost_Field 21 - Body
    try:
        Body = findSectionPContent.find(class_="body").text.lstrip().rstrip()

    except:
        Body = None
    post_list.append(Body)

    footer = soup.find("div", class_="footer")
    span = footer.find_all("span")

    # tblPost_Field 22 - InitialPostDate
    try:
        initial_post_date = span[1].text.split(":")[1].lstrip().rstrip()
    except:
        initial_post_date = None
    post_list.append(initial_post_date)

    # tblPost_Field 23 - RenewedDate
    try:
        renewed_date = span[2].text.split(":")[1].lstrip().rstrip()
    except:
        renewed_date = None
    post_list.append(renewed_date)

    class_a = findSectionPContent.find_all("div", class_="c")
    # tblPost_Field 24,25 - Class_1_Title,Class_1_Value
    try:
        Class_1_Title = class_a[0].find(class_="t").text.lstrip().rstrip()
        Class_1_Value = class_a[0].find(class_="i").text.lstrip().rstrip()
    except:
        Class_1_Title = None
        Class_1_Value = None
    post_list.append(Class_1_Title)
    post_list.append(Class_1_Value)

    # tblPost_Field 26,27 - Class_2_Title,Class_2_Value
    try:
        Class_2_Title = class_a[1].find(class_="t").text.lstrip().rstrip()
        Class_2_Value = class_a[1].find(class_="i").text.lstrip().rstrip()
    except:
        Class_2_Title = None
        Class_2_Value = None
    post_list.append(Class_2_Title)
    post_list.append(Class_2_Value)

    # tblPost_Field 28,29 - Class_3_Title,Class_3_Value
    try:
        Class_3_Title = class_a[2].find(class_="t").text.lstrip().rstrip()
        Class_3_Value = class_a[2].find(class_="i").text.lstrip().rstrip()
    except:
        Class_3_Title = None
        Class_3_Value = None
    post_list.append(Class_3_Title)
    post_list.append(Class_3_Value)

    # tblPost_Field 30,31 - Class_4_Title,Class_4_Value
    try:
        Class_4_Title = class_a[3].find(class_="t").text.lstrip().rstrip()
        Class_4_Value = class_a[3].find(class_="i").text.lstrip().rstrip()
    except:
        Class_4_Title = None
        Class_4_Value = None
    post_list.append(Class_4_Title)
    post_list.append(Class_4_Value)

    # tblPost_Field 32,33 - Class_5_Title,Class_5_Value
    try:
        Class_5_Title = class_a[4].find(class_="t").text.lstrip().rstrip()
        Class_5_Value = class_a[4].find(class_="i").text.lstrip().rstrip()
    except:
        Class_5_Title = None
        Class_5_Value = None
    post_list.append(Class_5_Title)
    post_list.append(Class_5_Value)

    # tblPost_Field 34,35 - Class_6_Title,Class_6_Value
    try:
        Class_6_Title = class_a[5].find(class_="t").text.lstrip().rstrip()
        Class_6_Value = class_a[5].find(class_="i").text.lstrip().rstrip()
    except:
        Class_6_Title = None
        Class_6_Value = None
    post_list.append(Class_6_Title)
    post_list.append(Class_6_Value)

    # tblPost_Field 36,37 - Class_7_Title,Class_7_Value
    try:
        Class_7_Title = class_a[6].find(class_="t").text.lstrip().rstrip()
        Class_7_Value = class_a[6].find(class_="i").text.lstrip().rstrip()
    except:
        Class_7_Title = None
        Class_7_Value = None
    post_list.append(Class_7_Title)
    post_list.append(Class_7_Value)

    # tblPost_Field 38,39 - Class_8_Title,Class_8_Value
    try:
        Class_8_Title = class_a[7].find(class_="t").text.lstrip().rstrip()
        Class_8_Value = class_a[7].find(class_="i").text.lstrip().rstrip()
    except:
        Class_8_Title = None
        Class_8_Value = None
    post_list.append(Class_8_Title)
    post_list.append(Class_8_Value)

    # tblPost_Field 40,41 - Class_9_Title,Class_9_Value
    try:
        Class_9_Title = class_a[8].find(class_="t").text.lstrip().rstrip()
        Class_9_Value = class_a[8].find(class_="i").text.lstrip().rstrip()
    except:
        Class_9_Title = None
        Class_9_Value = None
    post_list.append(Class_9_Title)
    post_list.append(Class_9_Value)

    # tblPost_Field 42,43 - Class_10_Title,Class_10_Value
    try:
        Class_10_Title = class_a[9].find(class_="t").text.lstrip().rstrip()
        Class_10_Value = class_a[9].find(class_="i").text.lstrip().rstrip()
    except:
        Class_10_Title = None
        Class_10_Value = None
    post_list.append(Class_10_Title)
    post_list.append(Class_10_Value)

    # tblPost_Field 44,45 - Class_11_Title,Class_11_Value
    try:
        Class_11_Title = class_a[10].find(class_="t").text.lstrip().rstrip()
        Class_11_Value = class_a[10].find(class_="i").text.lstrip().rstrip()
    except:
        Class_11_Title = None
        Class_11_Value = None
    post_list.append(Class_11_Title)
    post_list.append(Class_11_Value)

    # tblPost_Field 46,47 - Class_12_Title,Class_12_Value
    try:
        Class_12_Title = class_a[11].find(class_="t").text.lstrip().rstrip()
        Class_12_Value = class_a[11].find(class_="i").text.lstrip().rstrip()
    except:
        Class_12_Title = None
        Class_12_Value = None
    post_list.append(Class_12_Title)
    post_list.append(Class_12_Value)

    # tblPost_Field 48 - Class_More

    if len(class_a) > 11:
        post_list.append("Check post for more classes categories")
    else:
        post_list.append(None)

    # Search and add information about the user
    findSectionUinfo = soup.find("div", id="uinfo")

    # tblPost_Field 49 - UserReferenceNumber
    try:
        user_reference_number = findSectionUinfo.find("a")["href"].split("/")[2]
    except:
        user_reference_number = None
    post_list.append(user_reference_number)

    # tblPost_Field 50 - UserFullName
    try:
        user_fullname = findSectionUinfo.find("a").text.lstrip().rstrip()
    except:
        user_fullname = None
    post_list.append(user_fullname)

    # tblPost_Field 51 - UserRegisteredSince
    try:
        user_registered_since = findSectionUinfo.find(class_="since").text.lstrip().rstrip()[-10:]
    except:
        user_registered_since = None
    post_list.append(user_registered_since)

    # tblPost_Field 52 - UserProfileLink
    try:
        user_profile_link = "https://list.am" + findSectionUinfo.find("a")["href"]
    except:
        user_profile_link = None
    post_list.append(user_profile_link)

    counter = counter + 1

    # Adding to the database

    cursor_LISTAM_Active.execute(
        "Insert INTO Posts_Active VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        post_list)

    connection_LISTAM_Active.commit()
    print(str(total_number), "/", str(counter), "--added to the Posts_Active table: ", post_reference)

###Testing code
##        print("This is the line for post:", post_reference, "\n", post_list)
##        print("The number of elements in the record are:",str(len(post_list)), "\n")
##        print("\n")


# Find out how much time it took to save all images
Execution_Log = []
Execution_Log.append(timestamp)
end = time.perf_counter()
Execution_Log.append(round(end - start, 2))
Execution_Log.append(counter)

cursor_LISTAM_Active.execute("Insert INTO Execution_Log VALUES (?,?,?)", Execution_Log)
connection_LISTAM_Active.commit()
print(f"time taken {round(end - start, 2)}")

# Close database connection
connection_LISTAM_Active.close()