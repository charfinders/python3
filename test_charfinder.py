import pytest

from charfinder import parse, match, scan


@pytest.fixture
def line_for_A():
    return '0041;LATIN CAPITAL LETTER A;Lu;0;L;;;;;N;;;;0061;'


@pytest.fixture
def line_with_old_name():
    return '002E;FULL STOP;Po;0;CS;;;;;N;PERIOD;;;;'


@pytest.fixture
def three_lines():
    return ['003B;SEMICOLON;Po;0;ON;;;;;N;;;;;',
            '003C;LESS-THAN SIGN;Sm;0;ON;;;;;Y;;;;;',
            '003D;EQUALS SIGN;Sm;0;ON;;;;;N;;;;;']


def test_simple_parse(line_for_A):
    char, name = parse(line_for_A)
    assert char == 'A'
    assert name == 'LATIN CAPITAL LETTER A'


def test_parse_with_old_name(line_with_old_name):
    char, name = parse(line_with_old_name)
    assert char == '.'
    assert name == 'FULL STOP | PERIOD'


def test_parse_with_reduntant_old_name():
    line = '00BD;VULGAR FRACTION ONE HALF;No;0;ON;<fraction> 0031 2044 0032;;;1/2;N;FRACTION ONE HALF;;;;'
    char, name = parse(line)
    assert name == 'VULGAR FRACTION ONE HALF'


def test_match_one_word(line_for_A):
    char, name = parse(line_for_A)
    assert match(set(['CAPITAL']), name)


def test_match_two_words(line_for_A):
    char, name = parse(line_for_A)
    assert match(set(['CAPITAL', 'LATIN']), name)


def test_match_all_words(line_for_A):
    char, name = parse(line_for_A)
    assert match(set(name.split()), name)


def test_scan_one_word(three_lines):
    result = list(scan(three_lines, 'sign'))
    assert len(result) == 2
    char, name = result[0]
    assert char == '<'
    assert name == 'LESS-THAN SIGN'
    char, name = result[1]
    assert char == '='
    assert name == 'EQUALS SIGN'


def test_scan_one_word_in_hyphenated_name(three_lines):
    result = list(scan(three_lines, 'less'))
    assert len(result) == 1
    char, name = result[0]
    assert char == '<'
    assert name == 'LESS-THAN SIGN'


def test_scan_hyphenated_word(three_lines):
    result = list(scan(three_lines, 'less-than'))
    assert len(result) == 1
    char, name = result[0]
    assert char == '<'
    assert name == 'LESS-THAN SIGN'


def test_scan_empty_query(three_lines):
    result = list(scan(three_lines, ' '))
    assert len(result) == 0


def test_scan_old_name(line_with_old_name):
    result = list(scan([line_with_old_name], 'period'))
    assert len(result) == 1
    char, name = result[0]
    assert char == '.'
    assert name == 'FULL STOP | PERIOD'
