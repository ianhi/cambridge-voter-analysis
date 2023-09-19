# Data Source

The data for each year comes in two files (Voter List, Voter History) sourced from the Cambridge Elections commission. If you email `elections2@cambridgema.gov` you can request the raw data, I found them to be very friendly and responsive.

## Data cleaning

### Birthdays
There are several birthdays in the dataset that are clearly entered incorrectly (e.g. born in 0986, or born in 1812). For some birthdays it was clear how to correct them so I manually modified the data files

12GDA0186001  - 0986 -> 1986

The follow voter ids had entered the year wrong i.e. 0980 instead of 1980. I manually changed the millenia

- 04WDA0180001
- 12GDA0186001
- 01DML1591001
- 08WJB0481002


For birthdays that did not have an obvious year to correct to (e.g. 1812 -> ???) I excluded those voting records.


### Headers
I added headers to the CSV files for 2012 and 2011.
