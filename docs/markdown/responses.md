# Module `responses`

<a name='module-responses'></a>
*Generated on 2025-10-18T20:08:17*

## Module Data

<a name='responses-var-affirmatives'></a>
- **AFFIRMATIVES** = `['y', 'yes', 'yep', 'yup', 'yea', 'yeah', 'affirmative', 'sure', 'indeed', 'absolutely', 'certainly', 'of course', 'ok', 'okay', 'alright', 'roger', 'naturally', 'definitely', 'fine', 'correct', 'exactly', 'totally', 'cool']`
<a name='responses-var-negatives'></a>
- **NEGATIVES** = `['n', 'no', 'nope', 'nah', 'nay', 'never', 'negative', 'not', 'incorrect', 'wrong', 'none', 'refuse', 'decline', 'cannot', 'impossible', 'disagree', 'stop']`

## Function **normalize**

<a name='responses-function-normalize'></a>
```python
normalize(s)
```

Trim and lowercase a string for comparison.

## Function **is_affirmative**

<a name='responses-function-is_affirmative'></a>
```python
is_affirmative(s)
```

Return True if input matches a known affirmative response.

## Function **is_negative**

<a name='responses-function-is_negative'></a>
```python
is_negative(s)
```

Return True if input matches a known negative response.

