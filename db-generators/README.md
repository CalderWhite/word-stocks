Order of operations:

1. 
 - `gen_ratios.py`: Generates the ratios from one year to the next for each
                    year. Populates `yearly_ratios`.
 - `nlp.py`: Aggregates all the text from `stock_metadata`'s descriptions 
             into the `words` table with word tokenization.

2.
 - `build_scores.py`: Generates different scores for each word year by year. Some
                 of the scores are: median ratio, mean ratio, win percent
                 (how many stocks have a ratio >=1.0 that year).
