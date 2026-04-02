from csvsmith.utils.distance import StringDistance, Relation

def test_exact_match():
    res = StringDistance.analyze("hello", "hello")
    assert res.classification == Relation.EXACT_MATCH
    assert res.damerau_levenshtein_distance == 0
    assert res.similarity_percentage == 100.0

def test_case_insensitive_match():
    res = StringDistance.analyze("Hello", "hello")
    assert res.classification == Relation.CASE_INSENSITIVE_MATCH
    # analyze method calls classify first, which finds CASE_INSENSITIVE_MATCH
    # but for distance calculation it uses strings as-is unless ignore_case=True
    assert res.damerau_levenshtein_distance == 1 

def test_case_insensitive_match_with_ignore_case():
    res = StringDistance.analyze("Hello", "hello", ignore_case=True)
    assert res.classification == Relation.CASE_INSENSITIVE_MATCH
    assert res.damerau_levenshtein_distance == 0
    assert res.similarity_percentage == 100.0

def test_whitespace_trimmed_match():
    res = StringDistance.analyze("  hello  ", "hello")
    assert res.classification == Relation.WHITESPACE_TRIMMED_MATCH

def test_normalized_space_match():
    res = StringDistance.analyze("h e l l o", "hello")
    assert res.classification == Relation.NORMALIZED_SPACE_MATCH

def test_damerau_levenshtein_transposition():
    # transposition of 'ae' to 'ea'
    res = StringDistance.analyze("aabc", "abac")
    # 'aabc' -> 'abac' is one transposition of 'ab' at index 1,2? 
    # Wait: a-a-b-c vs a-b-a-c. 
    # index 1: a vs b
    # index 2: b vs a
    # This is a transposition.
    assert res.damerau_levenshtein_distance == 1

def test_jaro_winkler_score():
    res = StringDistance.analyze("martha", "marhta")
    assert res.jaro_winkler_score > 0.9
