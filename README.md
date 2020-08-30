# Anagram REST API
===========================================

## Implementation Notes

- I implemented this API using one Python module and the Flask microservice.
- I stored the provided dictionary.txt, as well as a datastore called words.txt, in the /resources directory.
- This API runs on 127.0.0.1:5000. So, for example, a curl instruction could be:

    - curl -i http://127.0.0.1:5000/anagrams/read.json

- Run a $pip install -r requirements.txt before running the API.


## Endpoints and Endpoint Notes

This API responds to 6 endpoints, listed here with notes:

- `POST /words.json`: Takes a JSON array of English-language words and adds them to the corpus (data store).
	- My data store is the file words.txt, included in the resources folder.
	- The example given in the original README.md did not include this, but I found that it is necessary
	  to escape any quotation marks in the JSON input, as well as exclude the leading and trailing single
 	  quotes. For example, a valid curl would be:
	$ curl -H "Content-Type: application/json" -i -X POST -d {\"words\":[\"read\",\"dear\",\"dare\"]} http://127.0.0.1:5000/words.json
- `GET /anagrams/:word.json`:
  - Returns a JSON array of English-language words that are anagrams of the word passed in the URL.
  - This endpoint should support an optional query param that indicates the maximum number of results to return.
	- This query param has been implemented as "limit"
	- I have also added an optional query param that indicates whether proper nouns can be included in
	  the list of returned anagrams.
- `DELETE /words/:word.json`: Deletes a single word from the data store.
	- This deletes from the file words.txt.
- `DELETE /words.json`: Deletes all contents of the data store.
	- This deletes from the file words.txt.

---Optional Endpoints---
- `GET /stats/stat`: Returns the desired statistic from data in the corpus.
	- Options are min, max, and avg, all referring to length of a single word in the corpus, and total,
	  which returns the number of words in the corpus.
- `DELETE /anagrams/word.json`: Deletes a single word, as well as all of its anagrams, from the data store
	- This deletes from the file words.txt.


## Run Instructions

I am on a Windows machine, but the instructions should be the same on OSX or Linux.
1. Open a terminal window and navigate to the Anagram-API directory. Run Anagram.py to start the server.
2. In a separate terminal window, run your curl command with the HTTP request you desire.

And that's it. You may view any words in the data store by viewing the words.txt file.
