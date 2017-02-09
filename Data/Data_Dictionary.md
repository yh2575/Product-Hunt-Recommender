# About the data
Scraped producthunt.com API for 20 GB of user data, product data, rating data, and comment data. In addition, I downloaded other data from data.world. 

## Rating data 
593185 ratings with 2573 users
and 42010 products

threshold: users > 50 ratings,
products > 10 ratings

## Post and User Files 

The best, most-current data files to use for offline Post and User Analysis are PostsForAnalysis.txt and UsersForAnalysis.txt. 

## AllTopics.csv

id - Topic ID number - for use in Product Hunt API requests
name - Topic name / 'slug'
description - Topic description
num_followers - Total number of followers (as of 11-29-2016)
num_posts - Total number of posts (as of 11-29-2016); note that many products are posted to more than one topic

## PostsForAnalysis.txt 
Columns 1 through 12 are:
id - Post ID number
date - Date in Month/Day/Year
day - 7 days of week: Sunday through Saturday
created_at - Date/Time in Year-Month-DayT00:00:00.000-8:00
time_of_day - 4 times of day: Morning, Afternoon, Evening, Night - described in more detail below
name - Post name
tagline - Post/product tagline
thumbnail_type - 4 thumbnail formats: Image, Video, Audio, Book Preview
product_state - 3 states: Default, Pre_launch, or No_Longer_Online
comments_count - Number of comments made on the post
num_makers - Number of makers of the product (0 denotes the maker is either not on Product Hunt or hasn't been tagged to the product)
num_topics - Number of topics in which the post was tagged

Columns 13 - 313 are all possible topics a post could be tagged within the timeframe of the data.
TRUE denotes the post was tagged in that topic
"No data" indicates FALSE; the post was not tagged in that topic

Columns 314 and 315 are:
user_id - the ID number of the user who posted the post
votes_count - total number of votes for the post

Time_of_day details

A new 'time_of_day' column was added, which is the time of day during which the post was created, using the following heuristic breakdown:

Morning: 5am to 11:59:59.999am
Afternoon: 12pm to 4:59:59.999pm
Evening: 5pm to 8:59:59.999pm
Night: 9pm to 4:59:59.999am
NOTE: All times in America/Los_Angeles timezone


## UsersForAnalysis.txt 

id - User ID number
created_at - Date/Time in Year-Month-DayT00:00:00.000-8:00
name - The user's name
username - The user's Product Hunt handle
headline - User headline - typically Title and Company but can be anything or nothing at all
twitter_username - User's Twitter handle (in the case they signed up via Twitter)
website_url - User's website
collections_count - Total number of collections for this user
followed_topics_count - Total number of topics this user follows
followers_count - Number of followers this user has
followings_count - Number of Hunters this user follows
maker_of_count - Number of products this user has made
posts_count - Number of products this user has hunted
votes_count - Number of votes this user has submitted

Timeframe of data

AllTopics.csv contains all topics, including their total number of followers and total number of posts within those topics as of 11-29-2016

UsersForAnalysis.txt contains all users as of 11-30-2016, except hidden users. UsersForExploration.csv contains 50,000 randomly-sampled rows from UsersForAnalysis.txt.

Although the data dump from the Product Hunt API included posts from dates 11-24-2014 to 11-23-2016, one week's worth of the most recent posts (from 11-17-2016 to 11-23-2016) were removed to create PostsForAnalysis.txt.
This week of posts was removed, because those posts had not been given ample time to receive votes, and thus would have on average fewer votes per post. Since the data contains plenty of posts across the two years, 
it is okay to remove them. 

source: data.world 
