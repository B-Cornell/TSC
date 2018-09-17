# Time Since Collision

In this project I am finding how long it has been since dark matter halos have been in a major merger event
The motivation behind this is to help us in thinking about relaxation times for galaxy clusters to help understand how we expect BCGs to wobble

---------------------

1. Getting our data sorted by mainleafid and x position

Code - SQL queries in the cosmosim.org database

Output - BigMDPL_6E13_\#(snapshot)\_x.csv and BigMDPL_6E13_\#(snapshot)\_mainleaf.csv

----------------------


2. Finding the separation distances between each halo at the many timesteps

Code - CloseHaloFinder.py

Input - CSVFiles_X/BigMDPL_6E13_\#(snapshot)\_x_.csv

Output - CloseHalos/close_halo_\#(snapshot).txt

----------------------

3. Attach all the close halos from the previous code to each individual halo at all the timesteps

Code - singletreehistory.py

Input - CloseHalos/close_halo_\#(snapshot).txt

Output - singletreehistory/singletreehistory\#(snapshot).pkl

----------------------

4. Look through the history and find all the actual mergers and record the details of the merger

Code - fulldata.py

Input - singletreehistory/singletreehistory\#(snapshot).pkl

Output - FullData/full_data_\#(snapshot).pkl

----------------------

5. Perform the data analysis to explore results

Code - tsc_analysis.py

Input - FullData/full_data_\#(snapshot).pkl

Output - Plots/\*
