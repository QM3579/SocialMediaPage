#!/usr/bin/python
import cgi
import sys
import csv
import cgitb;
cgitb.enable()

form = cgi.FieldStorage()

MemberList = open("http://cs.mcgill.ca/~xwang200/data/members.csv","r")
d = []
for line in MemberList.readlines():
	templine = line.rstrip()
	if templine.split(None, 1)[0] <> "name":
		d += [templine.split(None, 1)[0]]
MemberList.close()

TopicPost = open("http://cs.mcgill.ca/~xwang200/data/topic.csv","a")
if "post" in form:
	FilteredPost = ""
	Filter1 = form["post"].value.split(",")
	for a in range(0,len(Filter1)):
		Filter2 = Filter1[a].split("\n")
		for b in range(0,len(Filter2)):
			FilteredPost += Filter2[b]
			if b < len(Filter2)-1:
				FilteredPost = FilteredPost[:-1]
				FilteredPost += " "
	TopicPost.write(form["user"].value)
	TopicPost.write("\n")
	TopicPost.write(FilteredPost)
	TopicPost.write("\n")
TopicPost.close()

Tempall = ""
AddPrompt = ""
DebugHelper = ""
ValidFriend = "False"
AlreadyFriend = "False"
MRead = open("http://cs.mcgill.ca/~xwang200/data/members.csv","r")

if "add" in form:
	for line in MRead.readlines():
		templine = line.rstrip()
		if form["user"].value == form["add"].value:
			AddPrompt = "   You can't add yourself as a friend."
			break
		if templine.split(None, 1)[0] <> form["user"].value:
			if form["add"].value == templine.split(None, 1)[0]:
				ValidFriend = "True"
				AddPrompt = "   Friend successfully added!"
				break
			AddPrompt = "   The username you entered is invalid."
	if ValidFriend == "True":
		MRead.seek(0)
		for line in MRead.readlines():
			templine = line.rstrip()
			if templine.split(None,1)[0] == form["user"].value:
				for i in range(3,len(templine.split())):
					if templine.split()[i] == form["add"].value:
						AlreadyFriend = "True"
						AddPrompt = "   This user is already your friend."
						break
		if AlreadyFriend ==  "False":
			MRead.seek(0)
			for line in MRead.readlines():
				templine = line.rstrip()
				if templine.split(None,1)[0] == form["user"].value:
					Added = templine
					Added += " "
					Added += form["add"].value
					Added += "\n"
					Tempall += Added
				elif templine.split(None,1)[0] == form["add"].value:
					Added = templine
					Added += " "
					Added += form["user"].value
					Added += "\n"
					Tempall += Added
				else:
					Tempall += line
			MRead.close()
			MWrite = open("http://cs.mcgill.ca/~xwang200/data/members.csv","w")
			MWrite.write(Tempall)
			MWrite.close()
		else:
			MRead.close()
	else:
		MRead.close()

TopicFinal = ""
UserLine = ""
Topic = ""
Topiclimit = 10
Current = ""
Match = ""
MemberList = open("http://cs.mcgill.ca/~xwang200/data/members.csv","r")
TopicList = open("http://cs.mcgill.ca/~xwang200/data/topic.csv","r")

for line in MemberList.readlines():
	templine = line.rstrip()
	if form["user"].value == templine.split(None,1)[0]:
		UserLine = templine
		break

for row in reversed(list(csv.reader(TopicList))):
	if len(row) <> 0:
		Topic += row[0]
		Topic += "\n"

Tlist = Topic.split("\n")
for z in range(0,len(Tlist)):	
	if Current == "":
		Current = Tlist[z]
	else:
		Wlist = UserLine.split(" ")
		if Wlist[0] == Tlist[z]:
			Match = "True"
		for y in range(3,len(Wlist)):
			if Wlist[y] == Tlist[z]:
				Match = "True"
	if Match == "True":
		Topiclimit = Topiclimit - 1
		TopicFinal += "<h3>"
		TopicFinal += Tlist[z]
		TopicFinal += " said: "
		TopicFinal += Current
		TopicFinal += "</h3>"
		TopicFinal += "\n"
		Match = "False"
		Current = ""
	if Topiclimit == 0:
		break

MemberList.close()
TopicList.close()

UsersList = "List of users: "
for i in d:
	UsersList += i
	UsersList += ", "
UsersList = UsersList[:-2]
UsersList += "."

x='''<html>
<head>
<title>'''+form["user"].value+'''\'s Feed</title>
</head>
<body bgcolor="#99CCFF">
<table border="0" align="center" width="100%" style="margin: 0px auto;">
<tr>
<td width="40%">
<form name="addfriend" action="L.py" method="post">
<input type="hidden" name="user" value="'''+form["user"].value+'''">
Add friend:<input type="text" name="add">
<input type = "submit" value="Add">'''+AddPrompt+'''
</form>
<h4>'''+UsersList+'''</h4>
</td>
<td>
<a href="index.html"><h4 align="right">Log Out</h4></a>
</td>
</tr>
<tr>
<td colspan="2">
<center><h1>Welcome to your topics page, '''+form["user"].value+'''!</h1></center>
</td>
</tr>
<tr>
<td colspan="2">
<center><h2>Got anything on your mind? Share it with your friends!</h2></center>
</td>
</tr>
<tr>
<td colspan="2">
<form name="share" action="L.py" method="post">
<input type="hidden" name="user" value="'''+form["user"].value+'''">
<center><textarea name="post" rows=6 cols=50 wrap></textarea></center>
</td>
</tr>
<tr>
<td colspan="2">
<center><input type="submit" value="Post"></center>
</td>
</form>
</tr>
</table>
<center>'''+TopicFinal+'''</center>
</body>
</html>'''
print "Content-Type: text/html"
print "\n\n"
print x
