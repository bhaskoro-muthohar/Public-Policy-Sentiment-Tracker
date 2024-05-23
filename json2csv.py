import pandas as pd
from pandas import json_normalize

# Load the JSON data from the file
with open('tweets.json', 'r') as file:
    data = pd.read_json(file)

# Since data is already loaded as a DataFrame, directly normalize it if it contains deeply nested structures
# Flatten the 'user' dictionary along with the top-level structure
df = json_normalize(data.to_dict(orient='records'))

# Sometimes, normalizing directly doesn't handle deep nesting well,
# You might need to specify the record path or metadata if issues persist:
# df = json_normalize(data.to_dict(orient='records'), 
#                     record_path='user',
#                     meta=['tweet_id', 'id_str', 'url', 'date'],
#                     meta_prefix='tweet_')

# Save the DataFrame to a CSV file
df.to_csv('tweets.csv', index=False)
