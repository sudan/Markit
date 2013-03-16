Markit
======
Markit is an online social bookmarking site built using Redis as the only database with  Django( A web framework written
in python) jQuery and Backbone.js 

How to Use
==========

  1. Install Python and Django(1.x) 
  2. Install Redis and Redis client for Python(redis-py)
  3. Install sqlite3 and corresponding adapter for python(pysqlite)
  4. Download the repo and run the following command python manage runserver and navigate to localhost:8000 to visit the home page

Data Layout using Redis
=======================

There are mainly 5 objects namely
i.User 
  -- Represents a user object
ii.Bookmarks 
  -- Represents a bookmark
iii.Category 
  -- Represent a category for the bookmark corresponding to the user
iv.Tags 
  --Bookmarks are associated with tags and are visible to everyone 
v.Socialize
  -- Users can follow other users
  
  
1. User object

        i. SADD global:users:userId -- maintains global set of userIds 
        ii.SET userId:1:email -- email id corresponding to the userId 1
        iii.SET userId:1:username -- username corresponding to the userId 1
        iv. SET userId:1:first.name -- first name corresponding to the userId 1
        v. SET userId:1:last.name -- last name corresponding to the userId 1
        vi.SET userId:1:password -- password encrypted using bcrypt algo corresponding to the userId 1
        vii.SET userId:1:image -- gravatar image corresponding to the userId 1
        viii.SET userId:1:timestamp -- time when the userId 1 was created
        ix. SET userId:1:summary -- description about the userId 1
        x. SET username:sudan:userId -- reverse mapping for username and userId
        xi. SET email:ssudan16@gmail.com:userId --reverse mappnig of email required for authentication
        xii.SET auth.token:1233255asdv:userId -- reverse mapping of auth token required for authentication
        xiii.SET userId:1:auth.token -- auth token for the userId 1 which is also stored as a cookie n required for authentication

2.Bookmark Object

        i.SET bookmarkId:1:url -- bookmark url of  bookmarkId 1
        ii.SET bookmarkId:1:name -- bookmark name of bookmarkId 1
        iii.SET bookmarkId:1:description -- description for bookmarkId 1
        iv.SET bookmarkId:1:visibility -- public/private
        v.SET bookmarkId:1:created.date -- timestamp when bookmarkId  1 was created
        vi.SET bookmarkId:1:userId -- used to identify the owner of bookmark
        vii.SET bookmarkId:1:categoryId -- used to identify its category
        viii.LPUSH userId:1:bookmarks --bookmarks for the userId 1 maintained in the form of stack LIFO
        
        
3.Category Object

      i. SET categoryId:1:name -- name of the categoryId 1
      ii.SADD UserId:1:categoryId -- set of all category Ids corresponding to the userId 1
      iii.SADD userId:1:categoryName -- set of all categories corresponding to the userId 1
      iv.SET userId:1:categoryName:SOME_NAME:categoryId --reverse mapping to determine category name
      
4.Tag Object
  
      i.SET tagId:1:name -- name of the tagId 1
      ii.SET name:tag_name:tagId -- reverse mapping to determine tagId
      iii.SADD tagId:1:bookmarkIds --set of bookmarkIds corresponding to the tagId 1
      iv. SADD global:tags:tagId -- set of all tagIds
      
5.Socialize Object

    i. SADD userId:1:followers -- set of follower Ids corresponding to the userId 1
    ii.SADD userId:1:following -- set of people whom the userId 1 is following
    
Features
========

i.Users can create bookmarks and mark the visibility,edit and delete it
ii.User can create categories and group bookmarks based on categories and filter it
iii.User can add bookmarks to tags so that it is publicly available to others to follow it
iv.Multiple bookmarks can be added to same tag name by different users
v.User can follow other users
vi.User can add other user bookmarks to their list
vii.Add public bookmarks of following users
