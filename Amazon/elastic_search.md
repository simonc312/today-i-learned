# Elastic Search 

Use the _analyzer, _search endpoints usually running by default on localhost:9200 to test how input text queries are processed.

All analyzers are composed of **exactly one** Tokenizer which determines how input text is chunked such as by whitespace, nGram, etc. 

There are also Token Filters which can add, remove, or modify tokens based on criteria like common English language stop words such as 'the'. 

You can compose custom analyzers from different combinations of the basic components and reference the analyzer by name when performing a query. 

Currently queries for autocomplete suggestions seem to only accept prefixes and not suffixes. When querying with the word "Aunt" and the best match would be "Great Grant Aunt", it would not return any results because the score would be too low. 

There is a fuzziness factor which can be used to help return suggestion results when users misspell a word by applying an edit distance calculation. 