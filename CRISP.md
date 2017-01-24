# CRISP-DM:  Rec The Trail
_A Washington Trails Association Hike Recommender_

**The Cross Industry Standard Process for Data Mining (CRISP-DM) describes guidelines for data scientists who develop data products.**  

The steps for CRISP-DM and their respective application to Rec The Trail are described below.

![Image of CRISP-DM breakdown](img/crispdm.png)


## Business Understanding
The business understanding component of CRISP-DM requires collaborating data scientists and business professionals to clearly outline the business problem that they are trying to address.  At this point, the metrics used, definitions of success and timelines should also be established.  While there is not an obvious business application of a hike recommendation website, the goal of this project was to 1) Minimize the time that people are spending searching for a hike on the WTA website and 2) provide them with hikes that will most accurately meet their hiking style.


## Data Understanding
Data understanding encompasses data collection and initial exploratory data analysis.  As no dataset of the WTA hikes is readily available, the data was scraped using requests and BeautifulSoup with Python.  Features of interest that were collected included, but were not limited to, hike length, elevation gain, number of reports (a proxy for hike popularity), overall rating, hike description and location.  

As the project went on, one road block that I ran into is that only the average number of stars is reported for each hike, not the star rating for each user and trip report author.  This detracts from the overall recommendation model as limits the depth of user-item interactions and does not allow models to recommend based on similar users.  

![Graph of hikes w/ratings](img/starreviews.png)

Therefore, I decided to make my own rating data, based on sentiment analysis of trip reports. This text data also had to be scraped. With experience and time comes wisdom, so this round, I used requests, BeautifulSoup and MongoDB to store my data neatly. I tried multiple methods of sentiment analysis on my trip reports, which is further discussed in data preparation and modeling.  


## Data Preparation
Ah the favorite task of any data scientist- Data preparation.  This component covers all data cleaning that is required in order for the data to be used in the model.  Data preparation tasks included:
  - Getting drive time estimates for each hike based on longitude and latitude data using the Google Maps API
  - Creating dummy variables for hike features such as 'Lakes/Rivers', 'Summits', 'Allows dogs on leash'
  - Mapping identification numbers to all hikes and trip report authors
  - Normalize hike item data for use in recommendation model
  - Building rating dataset and item data datasets for the GraphLab models


## Modeling
Modeling and evaluation was required at three different points in the project: determining which hike features to include in the model, modeling sentiment analysis and building a custom rating system, and building the actual recommender system.

### Clustering and Feature Selection
Following feature extraction, I had a total of about 25 features.  In attempt to find clusters of hikes and potential trends, I applied PCA dimensionality reduction and used k-means (k-means ++) to cluster the hikes.  No matter the number of reduced features or clusters, it seemed that the only prominent feature that was clustered on was elevation gain.

![clustering](img/clusters.png)

![clustering](img/clusters2.png)

![clustering](img/clusters3.png)

In order to determine which features to include in my item content similarity model, I attempted multiple methods of feature selection, with average star rating as the endogenous variable, including:
  * Linear regression
  * Ridge regression
  * Lasso regression

### Hike Feature Importance
In order to get an idea of potential feature importance and weighting in my item content similarity recommender, I ran a Gradient Boosted model with all of my features as the exogenous variables and the average star rating as the exogenous variable.

![feature importance](img/featureimportance.png)


### Sentiment analysis
In order to create my user rating data, I applied sentiment analysis to trip report.  The following methods were used:
  * TextBlob polarity sentiment
  * Turi GraphLab built-in sentiment analysis model
  * Turi GraphLab sentiment analysis model trained on data scraped from everytrail.com
  *  Random Forests
  * Gradient Boosting
  * Adaboosting
    - With the following base estimators:
      * Multinomial bayes
      * Decision tree

The ratings were then grouped into 5, 3 or 1 (good, neutral or bad) based on their predicted probability of being a positive rating.

### Building the Recommender System

Once I had my rating data, I attempted multiple flavors of recommender systems in Turi Graphlab using both collaborative filter and item content similarity. The regularization parameters were tuned using RMSE and A/B testing.

For the final implementation of the model, I used a ranking factorization recommender with item data incorporated. However, due to poor recommendations given for new users, I decided to also incorporate an item content similarity based recommender into my web application for users with no data.

For users with no data and no hike to input for hike similarity recommendations, I use the baseline recommendations from the model based on hike popularity.

## Evaluation

### Hike Feature Importance
These models were evaluated with RMSE.

### Sentiment analysis
My sentiment analysis models were evaluated based on accuracy, precision and recall in a train/test split model.  
![SA model eval](img/samodels.png)

### Building the Recommender System
While the recommendation systems were largely evaluated using A/B testing from both myself and other hikers, I also considered RMSE and precision and recall at N.


## Deployment
The deployment phase of a data science project is the form in which the knowledge gained from the previous steps is communicated or the form in which the data project is released.  In some cases, this may just take the form of a report.  For Rec The Trail, what good is a recommendation system if people can't use it? Therefore, I had to also flex my web development skills and developed a web application for people to use.

### [Rec The Trail](http://recthetrail.com/)

![Image of the landing page](img/recthetrail.png)

On Rec The Trail application, a new user can input a rating from a hike and receive recommendations based on similar hikes.  Additionally, a returning user can come back, add in a new recommendation and get recommendations using the ranking factorization recommender.  The website also has some baseline recommendations for people who don't want to input any ratings.


## Next steps
* Use more advanced techniques on the trip report text to improve sentiment analysis based rating system
* Refine the web application (add weather report, add gear recommendations such as microspikes if snow is present).
* Allow user to change feature importance weight used in item content recommender.


## Sources

1) "Washington Trails Association." WTAs Blog. N.p., n.d. Web. 09 Aug. 2016.

2) "EveryTrail - Travel Community, IPhone Guides for Sightseeing, Hiking, Walking Tours and More." EveryTrail - Travel Community, IPhone Guides for Sightseeing, Hiking, Walking Tours and More. N.p., n.d. Web. 09 Aug. 2016.

3) Andy Bromberg. (n.d.). Retrieved August 09, 2016, from http://andybromberg.com/sentiment-analysis-python/

4) Debnath, S., Ganguly, N., & Mitra, P. (2008). Feature weighting in content based recommendation system using social network analysis. Proceeding of the 17th International Conference on World Wide Web - WWW '08. doi:10.1145/1367497.1367646

5) Machine Learning Blog & Software Development News. (n.d.). Retrieved August 09, 2016, from http://blog.datumbox.com/machine-learning-tutorial-the-naive-bayes-text-classifier/

6) Silva, Nádia, Estevam Hruschka, and Eduardo Hruschka. "Biocom Usp: Tweet Sentiment Analysis with Adaptive Boosting Ensemble." Proceedings of the 8th International Workshop on Semantic Evaluation (SemEval 2014) (2014): n. pag. Web.

7) Sobhanam, H., & Mariappan, A. K. (2013). Addressing cold start problem in recommender systems using association rules and clustering technique. 2013 International Conference on Computer Communication and Informatics. doi:10.1109/iccci.2013.6466121

8) Turi Machine Learning Platform User Guide. (n.d.). Retrieved August 09, 2016, from https://turi.com/learn/userguide/recommender/choosing-a-model.html
