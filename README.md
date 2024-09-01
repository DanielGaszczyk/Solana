# Solana

## Running the program
This program uses built-in Python functions, to run the program Python3 is required. 

- To run the main program
```
python3 index.py
```

- To run the scheduled script
```
python3 scheduled-task.py
```

- To generate mock data
```
python3 ./mock/generate-mock-data.py
```

## Limitations
During the implementation I noticed that the Solana Validation Client and API has some limitations.

- Rate limiters as I was allowed to send 10 requests before putting me in a timeout. that had an impact on getting the average block time.
- The lack of historical data, that made it impossible calculate the average validator count, as a work around.
    - I implemented a scheduled script that runs in the background and collects the validator count and block time every hour.
    - To be able to test the script i wrote another script that generates mock data for both validator count and block time.
- Solana doesn't prove any functions to get the block time, as a work around i used the "solana block-time" command which returns the slot and timestamp without milliseconds which in turn made it harder to count the average block time.
    - My initial solution was to write a function that sends a number of requests, segregates the data using the timestamp and counts how many new block were created in a second, then take the average to find the block_time.
    - To solve the rate limiter issue, I increased the number of requests and modified the resulting data to remove any incorrect or incomplete data for better results.
    

## Output
- The program outputs:
    - Current validators.
    - Latest block.
    - Average validators from the last 30 days.
    - Average block time from the last 30 days.
    - IP Clusters (exported to a file found in the "output" folder).
    - 2 line graphs to better show the results of the average validator count and block time (can be found in the "output" folder).

Example output (ran on mock data for the averages)
```
Validators: 1409
Lastest block: 287046608
Average validators: 1415.727536231884
Average Block time: 0.6029469565217391
IP clusters saved to ip-clusters.json
```
