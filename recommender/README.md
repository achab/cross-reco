**Recommender system, inspired by http://ampcamp.berkeley.edu/big-data-mini-course/movie-recommendation-with-mllib.html**

To compile the project, run
```
sbt assembly
```
Then, to launch an example of the project, run
```
spark-submit --driver-memory 2g --class MovieLensALS target/scala-*/movielens-als-assembly-*.jar src/main/resources/ml-1m src/main/resources/personalRatings.txt
```
