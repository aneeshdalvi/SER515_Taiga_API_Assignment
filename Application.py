import requests
import json
import sys
import datetime
import time

# Login authentication --- Enter your Password and Username for Taiga to get all the information
data = {"password": "", "username": "", "type": "normal"}
resp = requests.post('https://api.taiga.io/api/v1/auth', json=data)


token = ""
if resp.status_code != 200:
    print("Error")
else:
    print("Token - " + format(resp.json()["auth_token"]) + "\n")
    token = format(resp.json()["auth_token"])

data = {"AUTH_TOKEN": token}


# Accessing Taiga API by slug name For eg. "meng-ze-breitenburg-ser515" for your project ---
project_slug = input("Please enter your Taiga Slug :")
resp = requests.get('https://api.taiga.io/api/v1/projects/by_slug?slug=' + project_slug, json=data)

member_id = []
member_names = []
for values in resp.json():
    if(values == "slug"):
        print("Slug - " + resp.json()["slug"])

    if(values == "total_memberships"):
        print("\nThere are " + str(resp.json()["total_memberships"]) + " members in this project\n")

    if(values == "members"):
        print("The team members are - ")
        for members in resp.json()["members"]:
            member_id.append(members["id"])
            member_names.append(members["full_name"])
            print(members["full_name_display"] + ": " + members["role_name"])
           # print("Username - " + members["username"])

    if(values == "task_statuses"):
        for task_statuses in resp.json()["task_statuses"]:
            project_id = str(task_statuses["project_id"])

    if(values == "milestones"):
        for milestones in resp.json()["milestones"]:
            no_of_Sprints = len(milestones)

# print(member_names)
#print("\nOur ProjectID - " + project_id + "\n")

print("\nThere are total " + str(no_of_Sprints) + " Sprints in this project\n")


resp = requests.get('https://api.taiga.io/api/v1/milestones?project=' + project_id, json=data)
sprint_id = 0
sprint_name = []
milestones_id = []
userstories_id = []
userstories = {}
for values in resp.json():
    # if(insideValues == "estimated_start"):
    #     print("estimated_start - " + str(resp.json()["estimated_start"]))

    print(values["name"] + "\n")
    print("Sprint Id --> " + str(sprint_id))
    sprint_id = sprint_id + 1
    sprint_name.append(values["name"])
    userstories = values["user_stories"]
    milestones_id.append(values["id"])
    start_date = datetime.datetime.strptime(values["estimated_start"], '%Y-%m-%d')
    finish_date = datetime.datetime.strptime(values["estimated_finish"], '%Y-%m-%d')
    print("Estimated Start Date  -- " + start_date.strftime('%b %d,%Y'))
    print("Estimated Finish Date  -- " + finish_date.strftime('%b %d,%Y'))

    for us in values["user_stories"]:
        userstories_id.append(us["id"])

    closed_points = values["closed_points"]
    if(closed_points == "null"):
        print("Closed Points / Total Points  -- None / " + str(values["total_points"]))
    else:
        print("Closed Points / Total Points  -- " + str(closed_points) + " / " + str(values["total_points"]) + "\n")

#team member name variables to count the no of task assigned to each
josh = 0
aneesh = 0
viraj = 0
gangadhar = 0
abhi = 0
meng = 0
while range(1):
    sprint_id = input('Please choose a Sprint Id (mentioned above) to know more about it: ')
    # print(userstories_id[0])

    if sprint_id == str(0):
        print("\nGreat! You chose :" + sprint_name[0] + "\n")
        current_sprint = milestones_id[0]

        for values in resp.json():
            for us in values["user_stories"]:
                if(us["milestone"] == current_sprint):
                    no_of_userstories = len(values["user_stories"])
        print("No. of US in this sprint : " + str(no_of_userstories) + "\n")

        for values in resp.json():
            for us in values["user_stories"]:
                if(us["milestone"] == current_sprint):
                    print("US Name: " + us["subject"])
                    print("Is this US closed :" + str(us["is_closed"]))
                    # improve date format
                    tmp = us["created_date"]
                    new_date = ""
                    for i in tmp:
                        if(i != "T"):
                            new_date += i
                        else:
                            break
                    # changing date format
                    created_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                    print("US created :" + created_date.strftime('%b %d,%Y'))
                    user_story_id = us["id"]

                    nested_resp = requests.get('https://api.taiga.io/api/v1/history/userstory/' + str(user_story_id) + '?milestone=' + str(current_sprint), json=data)
                    for values in nested_resp.json():
                        for diff in values["values_diff"]:
                            if 'milestone' in diff:
                                moved_to_sprint = values["created_at"]
                    # improve date format
                    tmp = moved_to_sprint
                    new_date = ""
                    for i in tmp:
                        if(i != "T"):
                            new_date += i
                        else:
                            break
                    # changing date format
                    moved_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                    print("Moved to sprint : " + moved_date.strftime('%b %d,%Y') + "\n")

        # displaying tasks for particular users --
        josh = 0
        aneesh = 0
        viraj = 0
        gangadhar = 0
        abhi = 0
        meng = 0
        print("\nFetching all the tasks in Sprint 4 ...\n")
        assignedTo = {}

        task_resp = requests.get('https://api.taiga.io/api/v1/tasks?project=' + str(project_id) + '&milestone=' + str(current_sprint), json=data)
        for values in task_resp.json():
            if(values["milestone"] == current_sprint):
                    # no of tasks in that particular sprint
                no_of_tasks = len(task_resp.json())

        print("No. of Tasks in this sprint :" + str(no_of_tasks) + "\n")
        print("Displaying Tasks --> Assigned To" + "\n")

        for values in task_resp.json():
            if(values["assigned_to_extra_info"] is None):
                full_name_display = "None"
                task_name = values["subject"]
                member_name = "None"
            else:
                for assigned_to_extra_info in values["assigned_to_extra_info"]:
                    if 'full_name_display' in assigned_to_extra_info:
                        task_name = values["subject"]
                        assignedTo = values["assigned_to_extra_info"]
                        full_name_display = assignedTo['full_name_display']

                        if(full_name_display == "Josh Drumm"):
                            josh += 1
                        elif(full_name_display == "Viraj Talaty"):
                            viraj += 1
                        elif(full_name_display == "Abhishek Haksar"):
                            abhi += 1
                        elif(full_name_display == "GANGADHAR M"):
                            gangadhar += 1
                        elif(full_name_display == "Meng-Ze Chen"):
                            meng += 1
                        elif(full_name_display == "Aneesh Kiran Dalvi"):
                            aneesh += 1
                        else:
                            pass

            print("Task Name : " + task_name + " ----> " + full_name_display)

        print("\nFetching members data associated with no. of tasks assigned.. \n")
        for mem in member_names:
            if(mem == "Josh Drumm"):
                print("No. of Tasks assigned to " + mem + " -- " + str(josh))
            elif(mem == "Viraj Talaty"):
                print("No. of Tasks assigned to " + mem + " -- " + str(viraj))
            elif(mem == "Abhishek Haksar"):
                print("No. of Tasks assigned to " + mem + " -- " + str(abhi))
            elif(mem == "GANGADHAR M"):
                print("No. of Tasks assigned to " + mem + " -- " + str(gangadhar))
            elif(mem == "Meng-Ze Chen"):
                print("No. of Tasks assigned to " + mem + " -- " + str(meng))
            elif(mem == "Aneesh Kiran Dalvi"):
                print("No. of Tasks assigned to " + mem + " -- " + str(aneesh))
            else:
                pass

    elif sprint_id == str(1):

        print("\nNice! You chose :" + sprint_name[1] + "\n")
        current_sprint = milestones_id[1]

        for values in resp.json():
            for us in values["user_stories"]:
                if(us["milestone"] == current_sprint):
                    no_of_userstories = len(values["user_stories"])
        print("No. of US in this sprint : " + str(no_of_userstories) + "\n")

        for values in resp.json():
            for us in values["user_stories"]:
                if(us["milestone"] == current_sprint):
                    print("US Name: " + us["subject"])
                    print("Is this US closed :" + str(us["is_closed"]))
                    # improve date format
                    tmp = us["created_date"]
                    new_date = ""
                    for i in tmp:
                        if(i != "T"):
                            new_date += i
                        else:
                            break
                    # changing date format
                    created_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                    print("US created :" + created_date.strftime('%b %d,%Y'))
                    user_story_id = us["id"]

                    nested_resp = requests.get('https://api.taiga.io/api/v1/history/userstory/' + str(user_story_id) + '?milestone=' + str(current_sprint), json=data)
                    for values in nested_resp.json():
                        for diff in values["values_diff"]:
                            if 'milestone' in diff:
                                moved_to_sprint = values["created_at"]
                    # improve date format
                    tmp = moved_to_sprint
                    new_date = ""
                    for i in tmp:
                        if(i != "T"):
                            new_date += i
                        else:
                            break
                    # changing date format
                    moved_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                    print("Moved to sprint : " + moved_date.strftime('%b %d,%Y') + "\n")

        # displaying tasks for particular users --
        josh = 0
        aneesh = 0
        viraj = 0
        gangadhar = 0
        abhi = 0
        meng = 0
        print("\nFetching all the tasks in Sprint 3 ...\n")
        assignedTo = {}

        c = 0
        task_resp = requests.get('https://api.taiga.io/api/v1/tasks?project=' + str(project_id) + '&milestone=' + str(current_sprint), json=data)
        for values in task_resp.json():
            if(values["milestone"] == current_sprint):
                    # no of tasks in that particular sprint
                no_of_tasks = len(task_resp.json())

        print("No. of Tasks in this sprint :" + str(no_of_tasks) + "\n")
        print("Displaying Tasks --> Assigned To" + "\n")

        for values in task_resp.json():
            if(values["assigned_to_extra_info"] is None):
                full_name_display = "None"
                task_name = values["subject"]
                member_name = "None"
            else:
                for assigned_to_extra_info in values["assigned_to_extra_info"]:
                    if 'full_name_display' in assigned_to_extra_info:
                        task_name = values["subject"]
                        assignedTo = values["assigned_to_extra_info"]
                        full_name_display = assignedTo['full_name_display']

                        if(full_name_display == "Josh Drumm"):
                            josh += 1
                        elif(full_name_display == "Viraj Talaty"):
                            viraj += 1
                        elif(full_name_display == "Abhishek Haksar"):
                            abhi += 1
                        elif(full_name_display == "GANGADHAR M"):
                            gangadhar += 1
                        elif(full_name_display == "Meng-Ze Chen"):
                            meng += 1
                        elif(full_name_display == "Aneesh Kiran Dalvi"):
                            aneesh += 1
                        else:
                            pass

            print("Task Name : " + task_name + " ----> " + full_name_display)

        print("\nFetching members data associated with no. of tasks assigned.. \n")
        for mem in member_names:
            if(mem == "Josh Drumm"):
                print("No. of Tasks assigned to " + mem + " -- " + str(josh))
            elif(mem == "Viraj Talaty"):
                print("No. of Tasks assigned to " + mem + " -- " + str(viraj))
            elif(mem == "Abhishek Haksar"):
                print("No. of Tasks assigned to " + mem + " -- " + str(abhi))
            elif(mem == "GANGADHAR M"):
                print("No. of Tasks assigned to " + mem + " -- " + str(gangadhar))
            elif(mem == "Meng-Ze Chen"):
                print("No. of Tasks assigned to " + mem + " -- " + str(meng))
            elif(mem == "Aneesh Kiran Dalvi"):
                print("No. of Tasks assigned to " + mem + " -- " + str(aneesh))
            else:
                pass

    elif sprint_id == str(2):

        print("\nAwesome work! You chose :" + sprint_name[2] + "\n")
        current_sprint = milestones_id[2]

        for values in resp.json():
            for us in values["user_stories"]:
                if(us["milestone"] == current_sprint):
                    no_of_userstories = len(values["user_stories"])
        print("No. of US in this sprint : " + str(no_of_userstories) + "\n")

        for values in resp.json():
            for us in values["user_stories"]:
                if(us["milestone"] == current_sprint):
                    print("US Name: " + us["subject"])
                    print("Is this US closed :" + str(us["is_closed"]))
                    # improve date format
                    tmp = us["created_date"]
                    new_date = ""
                    for i in tmp:
                        if(i != "T"):
                            new_date += i
                        else:
                            break
                    # changing date format
                    created_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                    print("US created :" + created_date.strftime('%b %d,%Y'))
                    user_story_id = us["id"]

                    nested_resp = requests.get('https://api.taiga.io/api/v1/history/userstory/' + str(user_story_id) + '?milestone=' + str(current_sprint), json=data)
                    for values in nested_resp.json():
                        for diff in values["values_diff"]:
                            if 'milestone' in diff:
                                moved_to_sprint = values["created_at"]
                    # improve date format
                    tmp = moved_to_sprint
                    new_date = ""
                    for i in tmp:
                        if(i != "T"):
                            new_date += i
                        else:
                            break
                    # changing date format
                    moved_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                    print("Moved to sprint : " + moved_date.strftime('%b %d,%Y') + "\n")

        # displaying tasks for particular users --
        josh = 0
        aneesh = 0
        viraj = 0
        gangadhar = 0
        abhi = 0
        meng = 0
        print("\nFetching all the tasks in Sprint 2 ...\n")
        assignedTo = {}

        c = 0
        count_tasks = 0
        task_resp = requests.get('https://api.taiga.io/api/v1/tasks?project=' + str(project_id) + '&milestone=' + str(current_sprint), json=data)
        for values in task_resp.json():
            if(values["milestone"] == current_sprint):
                # no of tasks in that particular sprint
                no_of_tasks = len(task_resp.json())

        print("No. of Tasks in this sprint :" + str(no_of_tasks) + "\n")
        print("Displaying Tasks --> Assigned To" + "\n")

        for values in task_resp.json():
            if(values["assigned_to_extra_info"] is None):
                full_name_display = "None"
                task_name = values["subject"]
                member_name = "None"
            else:
                for assigned_to_extra_info in values["assigned_to_extra_info"]:
                    if 'full_name_display' in assigned_to_extra_info:
                        task_name = values["subject"]
                        assignedTo = values["assigned_to_extra_info"]
                        full_name_display = assignedTo['full_name_display']

                        if(full_name_display == "Josh Drumm"):
                            josh += 1
                        elif(full_name_display == "Viraj Talaty"):
                            viraj += 1
                        elif(full_name_display == "Abhishek Haksar"):
                            abhi += 1
                        elif(full_name_display == "GANGADHAR M"):
                            gangadhar += 1
                        elif(full_name_display == "Meng-Ze Chen"):
                            meng += 1
                        elif(full_name_display == "Aneesh Kiran Dalvi"):
                            aneesh += 1
                        else:
                            pass

            print("Task Name : " + task_name + " ----> " + full_name_display)

        print("\nFetching members data associated with no. of tasks assigned.. \n")
        for mem in member_names:
            if(mem == "Josh Drumm"):
                print("No. of Tasks assigned to " + mem + " -- " + str(josh))
            elif(mem == "Viraj Talaty"):
                print("No. of Tasks assigned to " + mem + " -- " + str(viraj))
            elif(mem == "Abhishek Haksar"):
                print("No. of Tasks assigned to " + mem + " -- " + str(abhi))
            elif(mem == "GANGADHAR M"):
                print("No. of Tasks assigned to " + mem + " -- " + str(gangadhar))
            elif(mem == "Meng-Ze Chen"):
                print("No. of Tasks assigned to " + mem + " -- " + str(meng))
            elif(mem == "Aneesh Kiran Dalvi"):
                print("No. of Tasks assigned to " + mem + " -- " + str(aneesh))
            else:
                pass

    elif sprint_id == str(3):

        print("\nSplendid! You choose :" + sprint_name[3] + "\n")
        current_sprint = milestones_id[3]

        for values in resp.json():
            for us in values["user_stories"]:
                if(us["milestone"] == current_sprint):
                    no_of_userstories = len(values["user_stories"])
        print("No. of US in this sprint : " + str(no_of_userstories) + "\n")

        for values in resp.json():
            for us in values["user_stories"]:
                if(us["milestone"] == current_sprint):
                    print("US Name: " + us["subject"])
                    print("Is this US closed :" + str(us["is_closed"]))
                    # improve date format
                    tmp = us["created_date"]
                    new_date = ""
                    for i in tmp:
                        if(i != "T"):
                            new_date += i
                        else:
                            break
                    # changing date format
                    created_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                    print("US created :" + created_date.strftime('%b %d,%Y'))
                    user_story_id = us["id"]

                    nested_resp = requests.get('https://api.taiga.io/api/v1/history/userstory/' + str(user_story_id) + '?milestone=' + str(current_sprint), json=data)
                    for values in nested_resp.json():
                        for diff in values["values_diff"]:
                            if 'milestone' in diff:
                                moved_to_sprint = values["created_at"]
                    # improve date format
                    tmp = moved_to_sprint
                    new_date = ""
                    for i in tmp:
                        if(i != "T"):
                            new_date += i
                        else:
                            break
                    # changing date format
                    moved_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                    print("Moved to sprint : " + moved_date.strftime('%b %d,%Y') + "\n")

        # displaying tasks for particular users --
        josh = 0
        aneesh = 0
        viraj = 0
        gangadhar = 0
        abhi = 0
        meng = 0
        print("\nFetching all the tasks in Sprint 1 ...\n")
        assignedTo = {}

        c = 0
        task_resp = requests.get('https://api.taiga.io/api/v1/tasks?project=' + str(project_id) + '&milestone=' + str(current_sprint), json=data)
        for values in task_resp.json():
            if(values["milestone"] == current_sprint):
                    # no of tasks in that particular sprint
                no_of_tasks = len(task_resp.json())

        print("No. of Tasks in this sprint :" + str(no_of_tasks) + "\n")
        print("Displaying Tasks --> Assigned To" + "\n")

        for values in task_resp.json():
            if(values["assigned_to_extra_info"] is None):
                full_name_display = "None"
                task_name = values["subject"]
                member_name = "None"
            else:
                for assigned_to_extra_info in values["assigned_to_extra_info"]:
                    if 'full_name_display' in assigned_to_extra_info:
                        task_name = values["subject"]
                        assignedTo = values["assigned_to_extra_info"]
                        full_name_display = assignedTo['full_name_display']

                        if(full_name_display == "Josh Drumm"):
                            josh += 1
                        elif(full_name_display == "Viraj Talaty"):
                            viraj += 1
                        elif(full_name_display == "Abhishek Haksar"):
                            abhi += 1
                        elif(full_name_display == "GANGADHAR M"):
                            gangadhar += 1
                        elif(full_name_display == "Meng-Ze Chen"):
                            meng += 1
                        elif(full_name_display == "Aneesh Kiran Dalvi"):
                            aneesh += 1
                        else:
                            pass

            print("Task Name : " + task_name + " ----> " + full_name_display)

        print("\nFetching members data associated with no. of tasks assigned.. \n")
        for mem in member_names:
            if(mem == "Josh Drumm"):
                print("No. of Tasks assigned to " + mem + " -- " + str(josh))
            elif(mem == "Viraj Talaty"):
                print("No. of Tasks assigned to " + mem + " -- " + str(viraj))
            elif(mem == "Abhishek Haksar"):
                print("No. of Tasks assigned to " + mem + " -- " + str(abhi))
            elif(mem == "GANGADHAR M"):
                print("No. of Tasks assigned to " + mem + " -- " + str(gangadhar))
            elif(mem == "Meng-Ze Chen"):
                print("No. of Tasks assigned to " + mem + " -- " + str(meng))
            elif(mem == "Aneesh Kiran Dalvi"):
                print("No. of Tasks assigned to " + mem + " -- " + str(aneesh))
            else:
                pass
    else:
        print("Invalid input....Please enter a valid sprint id")

    # Continuation of the application
    answer = input('\nDo you want to know more about other Sprints?: (Y / N)')

    if(answer == "Y" or answer == "y"):
        continue
    elif answer == "N" or answer == "n":
        break
    else:
        while True:
            print("\nInvalid input...Please enter a valid input (Y/N) \n")
            answer = input('Do you want to know more about other Sprints?: (Y / N)')
            if(answer == "Y" or answer == "y" or answer == "N" or answer == "n"):
                break
    if(answer == "N" or answer == "n"):
        break
