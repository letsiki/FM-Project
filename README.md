TODO's

create attribute correlations to other stats not just average rating
for example goals scored, assists, tackles won, headers won etc.

it seems that just adding positions without specifying roles is not particularly helpful the results are pretty weird

Unfortunately this is not possible I need to figure out something else maybe adding an assistant manager would do the trick
In the meanwhile I added the hidden attributes to the view. It will take place in my next exports

Ok assistant helped I can add a new manager once the sim is over. Now I am getting more interesting results

currently goes through all roles assumung edit search is open. This is not good enough I need to open it each time

I have gone a long way. Yet I am not happy with the correlations as I am not getting very meaningful results.
I will try to do specific correlations for example goals scored attacker positions and attribute correlation

Conversion rate seems to be pretty indipendent of attacker attributes! Perhaps I can do something else

create a dataframe where each row is basically a team

To create a single row of data we create a dataframe with all players of the team we keep the top 15 in appearances that are not goalkeepers
If there are not 15 we skip the team
Then we calculate the average conversion rate of the top goalscorer
and the average attributes of the rest of the team
And now er have a row of data

TO go through all the teams I need to create a macro

No I have the function to find correlations and also the function to test a dataset against a correlation

Now I want to find ways to use this in the game. For example I  can find correlation for each role and then 
use this to predict rating on a dataset I got from a scout or player search


