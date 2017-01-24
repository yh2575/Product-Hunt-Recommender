# Product-Hunt-Recommender
Recommendation systems use a number of different technologies. We can
classify these systems into two broad groups.

- Content-based systems examine properties of the items recommended. For
instance, if a Netflix user has watched many cowboy movies, then recom-
mend a movie classified in the database as having the “cowboy” genre.
- Collaborative filtering systems recommend items based on similarity mea-
sures between users and/or items. The items recommended to a user are
those preferred by similar users.

The data itself is represented as a utility matrix, giving for each user-item pair, a value that represents
yes for upvote. I assume that the matrix is sparse, meaning that most entries are “unknown”, especially there are 
so many new products everyday. 

The goal of a recommendation system is to predict the blanks in the utility
matrix. I need to design my recommendation system to take into account properties of products, such as tagline,
time_of_day, day_of_week were published, product names, maker info, categories, other user comments...
or to take into user properties, such as occupation, followings, followers, comments, liked topics... 

If so, I might then note the similarity between p1 and p2, and then conclude that since user1 upvoted p1, she/he
is likely to upvote p2 as well. 

In essense, out of all the new products coming out of each day, I want to suggest users the ones that similar to the products they upvoted before. 



