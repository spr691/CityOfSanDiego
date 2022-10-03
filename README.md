# CityOfSanDiego


Resource Allocation Prompt

Datasets Used
get_it_done_requests_closed_2016_datasd.csv (data.sandiego.gov)
get_it_done_requests_closed_2017_datasd.csv (data.sandiego.gov)
get_it_done_requests_closed_2018_datasd.csv (data.sandiego.gov)
get_it_done_requests_closed_2019_datasd.csv (data.sandiego.gov)
get_it_done_requests_closed_2020_datasd.csv (data.sandiego.gov)
get_it_done_requests_closed_2021_datasd.csv (data.sandiego.gov)
get_it_done_requests_closed_2022_datasd.csv (data.sandiego.gov)
get_it_done_requests_open_datasd (data.sandiego.gov)
pd_collisions_datasd_v1 (data.sandiego.gov)
ACSST5Y2020.S1903-Data (data.census.gov)

The Get It Done data and Collision data is easily accessible from the San Diego data repository.  Search for those keywords and the data will show up.  The census bureau data was a little more difficult to attain since there is so much data on their website.  I ended up searching for the dataset titled “S1903: MEDIAN INCOME IN THE PAST 12 MONTHS (IN 2021 INFLATION-ADJUSTED DOLLARS)” and then filtered it down to ACS 5-Year estimates, and then filtered it down to only CA zipcodes.  From there you can download a csv file.

Methodology
For this project, I aimed to analyze data pertaining to streetlight repair tickets that were submitted through the Get It Done app, and determine a systematic process, with an emphasis on equity and safety, that can be implemented to guide the Transportation Department.  I narrowed down the focusing on specific and trackable events which address the requirements of our key stakeholders.  For the focus on equity, I pulled median household income from the US Census Bureau and used that to assess any correlation between income and work requests.  Specifically, I looked at how many requests are coming in for each zipcode, and how long work requests are staying open for each zipcode.  The idea here is that from an equity perspective, we want to ensure that repairs are conducted equitably across all economic tiers in the city.  For the focus on safety, I pulled the Police Department’s Collision report from the San Diego data repository to assess the correlation between where the work requests are coming from and where the least safe streets are.  The idea here is that we have evidence of where safety mishaps are occurring, and we need to make sure to conduct repairs that address know hazards.  I chose to use zipcode as the geographical representation to group where tickets were generated, where tickets were closed, where different median incomes exist, and where collisions have been reported.

I setup my project using python scripts.  Pandas was used to ingest the data into dataframes and perform the necessary aggregations, sorting, and joining.  Numpy was used for mathematical functions.  Glob was used to read in numerous csv files.  Matplotlib was used for visualizations.  The main script for ingesting and processing all the data is called streetlights.py

I ingested and cleaned the Get It Done data first.  Since all closed and open datasets share the same schema, I was able to read them all into a list of Pandas dataframes, and then merge them together without any conflict or schema modifications.  There was a lot of unnecessary data, so I filtered for only data where the “service_name” was “Street Light Maintenance”. I then split up this data into 2 separate dataframes – one for closed requests and one for open.  Closed requests were filtered for “status” being equal to “Closed” or “Referred.”  Open requests were filtered for “status” being equal to “In Process” or “New.”  Then, for both of those datasets, I grouped by zipcode and counted all requests.  Then using the total counts, I added a rank for each zipcode.  The higher rank means more requests.  I also created a third dataframe from this data to represent the average case age by zipcode.  This was done by grouping closed Get It Done requests by zipcode, and then taking the mean of their “case_age_days.”  This was also ranked, and a higher rank means a higher average number of days for requests to be open. 

I ingested and cleaned the Collision data next.  It was also in csv format and was easy to pull into a Pandas dataframe.  However, upon inspection of the data, I determined that the address format was very different from how it is saved in the Get It Done data.  In the Collision data, there are separate columns for “address_road” and “address_sfx”, whereas the Get It Done data has the address in one long string containing unit, street, city, state, and zipcode.  In order to join the two datasets on zipcode, I needed to enrich the collisions data with zipcode.  I did this by writing a function that uses loops to find a “street_address” in the Get It Done data which contains the “address_road” from the Collision data.  If I found a match, then I took the zipcode from the Get It Done data and added it to the Collision data.  I then dropped any rows that were unable to find a zipcode.  From here, I was able to group by zipcode, calculate total counts, and add a rank for each zipcode.  Higher rank equates to higher volume of collision reports.  The function used to determine zipcodes is found in the script titled safety.py.   

The last data to ingest was the Median Income data from the US Census Bureau.  After finding the dataset as described in the Datasets section, I read in the csv file to a Pandas dataframe. There was a ton of unnecessary data, but when I determined which column contained household_income, I was able to narrow it down to “zipcode” and “median_income”.  The “median_income” was in a string format, where null values were represented by a “-“ character, “,” characters were used in large numbers, and a “+” character was used for zipcodes where the value was greater than $250,000.  Once I removed those characters, I was able to drop null rows, and add a rank for each zipcode.  Higher rank equates to higher median_income 

After all the data was ready, I joined all 5 dataframes on the “zipcode” column to have one concise dataframe with all the aggregations and ranking data.  I wrote this dataframe out to a csv file named “transportation_report.csv” because I believe it will be much more useful for the Transportation Department to draw conclusions and make decisions from.  I also used Matplotlib to make several visualizations to describe trends in the data.  These can be found in visualizations.py

To run the whole process, follow these steps:

1.	python3 safety.py
2.	python3 streetlights.py
3.	pyton3 visualizations.py
