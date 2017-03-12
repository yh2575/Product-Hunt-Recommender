# Motivation
producthunt.com is a tech product newsfeed website. It currently shows all the users the same content. I want to build a recommendation system to include users' preferences, something like Pandora's recommenders. This is to aim improving user experince and helping reduce customer churn.

# Background Knowledge
## Product-Hunt-Recommender
Recommendation systems use a number of different technologies. We can classify these systems into two broad groups.

- Content-based systems examine properties of the items recommended. For
instance, if a Netflix user has watched many cowboy movies, then recommend a movie classified in the database as having the “cowboy” genre.
- Collaborative filtering systems recommend items based on similarity measures between users and/or items. The items recommended to a user are those preferred by similar users.

The data itself is represented as a utility matrix, giving for each user-item pair, a value that represents
yes for upvote. I assume that the matrix is sparse, meaning that most entries are “unknown”, especially there are 
so many new products everyday. 

The goal of a recommendation system is to predict the blanks in the utility
matrix. I need to design my recommendation system to take into account properties of products, such as tagline,
time_of_day, day_of_week were published, product names, maker info, categories, other user comments...
or to take into user properties, such as occupation, followings, followers, comments, liked topics... 

If so, I might then note the similarity between p1 and p2, and then conclude that since user1 upvoted p1, she/he
is likely to upvote p2 as well. 

In essense, out of all the new products coming out of each day, I want to suggest users the ones that similar to the products they upvoted before. It may not even be necessary to find all items with the highest expected
ratings, but only to find a large subset of those with upvotes.

## Data
Scraped producthunt.com API for 20 GB of user data, product data, rating data, and comment data. In addition, I downloaded other data from data.world.<br>
593185 ratings with 2573 users and 42010 products<br>
threshold: users > 50 ratings, products > 10 ratings

## Tools
Python, HTML, CSS<br>
Matrix Factorization, Item-Content-recommender, Graphlab<br>
Flask 

## Models
### Item-content recommender 
based on 350 + features and 18000 + products<br>
important features of products: time of the day, day of the week, categories, number of votes

### Ranking matrix factorization recommender
593185 ratings with 2573 users and 42010 products <br>
threshold: users > 50 ratings, products > 10 ratings

## Validation
Local checks by randomly selecting product id and compare with the recommendations<br> 
Local checks by randomly selecting a user id and make sense of the recommendations by comparing with the user's online profile 

## Results
For Ranking matrix factorization recommender, users get a diverse range of recommendations. Users’ interest and interactions with the website are captured<br>
For Item-content recommender,users get top 5 most similar products of
their interest.  
