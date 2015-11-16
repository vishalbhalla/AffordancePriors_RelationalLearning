#!/usr/bin/python
'''
Created on 14 April 2011.
Author: Oscar Sjoberg.
v0.0.1

The Python style guide is used:
http://www.python.org/dev/peps/pep-0008/
'''
import itertools
import re
import sys
import time

def write_tuffy_network(lines, evidence_atoms, out_file_name):
    '''
    Write a Tuffy Markov Logic Network.
    '''
    # Open file.
    file = open(out_file_name, 'w')

    def write_line(line_tokens, gnd_map=None, file=file):
        '''
        Write a line to the output file.
        '''
        for token in line_tokens:
            # Write token.
            if isinstance(token, Atom):
                # Write atom.
                arguments = ', '.join([((gnd_map[variable] if variable.is_grounded and gnd_map else variable.name)) for variable in token.terms])
                file.write("%s(%s)" % (token.predicate_name, arguments))
            elif isinstance(token, Connective):
                # Write connective.
                if isinstance(token, Conjunction): file.write(", ")
                elif isinstance(token, Disjunction): file.write(" v ")
                elif isinstance(token, Implication): file.write(" => ")
                elif isinstance(token, Equivalence): file.write(" <=> ")
                elif isinstance(token, Negation): file.write("!")
            elif isinstance(token, Weight):
                # Write weight.
                if isinstance(token, SoftWeight): file.write("%s " % token.magnitude)
                elif isinstance(token, HardWeight): file.write(".")
            elif isinstance(token, Bracket):
                # Write bracket.
                if isinstance(token, LeftParenthesis): file.write("(")
                elif isinstance(token, RightParenthesis): file.write(")")
            elif isinstance(token, Symbol):
                # Write mathematical symbol.
                if isinstance(token, EqualitySign): file.write(" = ")
                elif isinstance(token, PlusSign): file.write(" + ")
                elif isinstance(token, MinusSign): file.write(" - ")
            # Write term.
            elif isinstance(token, Term): file.write(token.name)
            # Write line comment.
            elif isinstance(token, LineComment): file.write("// " + token.text)
        file.write('\n')

    def nested_lists_to_list(list_of_list):
        '''
        Merges the lists of a list of lists.
        '''
        return [item for list in list_of_list for item in list]

    def get_vars_to_ground_in_atom(atom):
        '''
        Get variables to ground in an atom.
        '''
        f = lambda term: isinstance(term, Variable) and term.is_grounded
        return filter(f, atom.terms)

    def get_vars_to_ground_in_line(line_tokens):
        '''
        Get variables to ground in a line.
        '''
        atoms = filter(lambda token: isinstance(token, Atom), line_tokens)
        return nested_lists_to_list([get_vars_to_ground_in_atom(atom) for atom in atoms])

    def get_vars_to_ground_in_file(token_lists):
        '''
        Get variables to ground in a file.
        '''
        vars_to_ground = nested_lists_to_list([get_vars_to_ground_in_line(token_list) for token_list in token_lists])
        return list(set(vars_to_ground))

    def get_constant_map(vars_to_ground):
        '''
        Compile a map where the keys are variables and the values are
        lists of constant assignments.
        '''
        var_constants_map = {}
        # Create key function for sorting lists of strings with embedded.
        # Horribly compact, but sorts both by number, without going 1, 10, 2
        # etc., and by alphabetic characters.
        # This makes zero padding constant names unnecessary for good looking
        # files.
        get_parts = lambda s: [part for parts in re.findall(r"([A-Za-z_]+)|(\d+)", s) for part in parts]
        key = lambda s: map(lambda t: int(t) if t.isdigit() else t, filter(lambda p: p, get_parts(s)))
        # Create the dictionary items.
        for var in vars_to_ground:
            # Retrieve atoms in evidence with the same predicate name as the atom for the variable under scrutiny
            atom_filter = lambda a: var.atom.predicate_name == a.predicate_name
            atoms = filter(atom_filter, evidence_atoms)
            # The index of the variable / constant as an argument to their atom.
            index = var.atom.terms.index(var)
            # Retrieve the constant at the index for each atom collected just above.
            # To use regular lexical sorting, simply don't supply the key
            # function bellow.
            constants = sorted(set([atom.terms[index].name for atom in atoms]), key=key)
            # Bind key and value in the map.
            var_constants_map[var] = constants
        return var_constants_map

    def list_product(li):
        '''
        Calculate the product of elements in a list.
        '''
        # Tip seen here: http://www.brankovukelic.com/post/626814926/calculate-product-of-list-items-python
        return li.pop() * list_product(li) if li else 1

    # Retrieve the constant map for looking up constants for each variable to
    # ground.
    print >>sys.stderr, "Building constant map...",
    start_time = time.time()
    constant_map = get_constant_map(get_vars_to_ground_in_file(lines))
    time_elapsed = time.time() - start_time
    print >>sys.stderr, "Done in %f s.\n" % time_elapsed
    # Write out file.
    for line in lines:
        vars_to_ground = get_vars_to_ground_in_line(line)
        if vars_to_ground:
            # Expand a formula.
            print >>sys.stderr, "Expanding formula: ",
            write_line(line, file=sys.stderr)
            # Retrieve all possible permutations.
            print >>sys.stderr, "Compiling permutations for formula...",
            permutations = get_permutations([constant_map[var] for var in vars_to_ground])
            print >>sys.stderr, "Done."
            start_time = time.time()
            # Calculate number of permutations.
            perm_size = list_product([len(constant_map[var]) for var in vars_to_ground])
            print >>sys.stderr, "Writing %d permutations... " % (perm_size),
            # Write permutations to the file.
            for permutation in permutations:
                # For each permutation create a map, were the keys are
                # variables and values are constants.
                gnd_map = dict(zip(vars_to_ground, permutation))
                # Write formula
                write_line(line, gnd_map=gnd_map)
            time_elapsed = time.time() - start_time
            print >>sys.stderr, "Done expanding formula."
            print >>sys.stderr, "Time elapsed: %f s.\n" % time_elapsed
        else:
            write_line(line)

    print >>sys.stderr, "Done!"
    # Close file.
    file.close()

def parse_evidence(file_name):
    '''
    Parses an evidence file and returns the evidence atoms.
    '''
    file = open(file_name, 'r')
    lines = filter(lambda line: line and line.strip() != '', file)
    def strip(s):
        return s.strip().strip('!')
    atoms = [Atom.build(strip(line))[0] for line in lines]
    return atoms

def parse_file(file_name):
    '''
    Parses a file containing an MLN.
    '''
    file = open(file_name, 'r')
    parsed_lines = [parse_line(line) for line in file]
    file.close()
    return parsed_lines

def parse_line(line):
    '''
    Parses a line.
    '''
    tokens = []

    def chunk(s, token_class):
        '''
        Take a chunk out of a string.
        '''
        # Remove leading whitespaces.
        s = s.lstrip()
        result = token_class.build(s)
        if result:
            token, s = result
            tokens.append(token)
        return (s, True) if result else (s, False)

    # Remove leading and trailing whitespaces.
    line = line.strip()

    # Do the parsing.
    while True:
        # Try to chunk out an atom.
        line, chunked = chunk(line, Atom)
        if chunked: continue
        # Try to chunk out a connective.
        line, chunked = chunk(line, Connective)
        if chunked: continue
        # Try to chunk out bracket.
        line, chunked = chunk(line, Bracket)
        if chunked: continue
        # Try to chunk out weight.
        line, chunked = chunk(line, Weight)
        if chunked: continue
        # Try to chunk out comment.
        line, chunked = chunk(line, Comment)
        if chunked: continue
        # Try to chunk out symbol.
        line, chunked = chunk(line, Symbol)
        if chunked: continue
        # Try to chunk out term.
        line, chunked = chunk(line, Term)

        # If nothing was chunked, return.
        if not chunked:
            return tokens

def get_permutations(lists):
    '''
    Calculate permutations given a list of lists whose elements should permutated.
    '''
    return itertools.product(*lists)

class Token(object):
    '''
    Base class representing a token.
    '''

    @staticmethod
    def build(s):
        '''
        Should be overridden and return a tuple, consisting of the token
        object, and the rest of the string that wasn't used when building
        the token.
        '''
        pass

class Term(Token):
    '''
    Class representing a term.
    '''

    def __init__(self, atom):
        self._atom = atom
        self._index = None
        self._name = None

    def get_index(self):
        return self._index

    def set_index(self, value):
        self._index = value

    @property
    def name(self):
        return self._name

    @property
    def atom(self):
        return self._atom

    index = property(get_index, set_index, "The index of the term in the argument.")

    @staticmethod
    def build(s):
        # Build constant if s matches a constant (number or string beginning
        # with majuscule).
        matches = filter(lambda m: m, [re.match(r"\d+\.?\d*", s), re.match(r"[A-Z]\w+", s)])
        if matches:
            const = matches[0].group(0)
            return Constant(const), s[len(const):]
        # Build variable if s matches a variable.
        matches = re.match(r"\w+", s)
        if matches:
            var = matches.group(0)
            return Variable(var), s[len(var):]

class Constant(Term):
    '''
    Class for representing terms.
    '''

    def __init__(self, s, atom=None):
        super(Constant, self).__init__(atom)
        self._name = re.sub('\W+', '', s)

    @staticmethod
    def is_constant(s):
        '''
        Return true if string s may be regarded as a constant.
        '''
        return re.match(r"[A-Z0-9]", s)

class Variable(Term):
    '''
    Class for representing terms.
    '''

    def __init__(self, s, atom=None):
        super(Variable, self).__init__(atom)
        self._name = re.sub('\W+', '', s)
        self._is_grounded = (s[:1] == '+')
        self._atom = atom

    @property
    def is_grounded(self):
        return self._is_grounded

    @staticmethod
    def is_variable(s):
        '''
        Return true if string s may be regarded as a variable.
        '''
        return re.match("\+?[a-z]", s)

    def __hash__(self):
        if not self._atom:
            return hash(self.name)
        return hash(self._atom.predicate_name) * 10 ** 7 + self.index #self._atom.terms.index(self)

    def __eq__(self, other):
        if not self._atom or not other._atom:
            return self == other
        is_same_index = (self.index == other.index)
        is_in_same_predicate = (self._atom.predicate_name == other._atom.predicate_name)
        return is_same_index and is_in_same_predicate

class Atom(Token):
    '''
    Class for representing atoms.
    '''
    def __init__(self, s):
        subtokens = Atom.parse(s)
        self._predicate_name = subtokens[0]
        self._terms = [self.build_term(token) for token in subtokens[1:]]
        # Set indexes.
        for term in self._terms:
            term.index = self._terms.index(term)

    @property
    def predicate_name(self):
        return self._predicate_name

    @property
    def terms(self):
        return self._terms

    @staticmethod
    def parse(s):
        return filter(lambda t: t, re.split('[^\w^!^\+]+', s))

    def build_term(self, s):
        if Variable.is_variable(s):
            return Variable(s, atom=self)
        elif Constant.is_constant(s):
            return Constant(s, atom=self)

    @staticmethod
    def build(s):
        matches = re.match("\w+\([^\)]+\)", s)
        if matches:
            return Atom(matches.group(0)), s[len(matches.group(0)):]

# Define connective classes.
class Connective(Token):
    '''
    Base class representing connectives.
    '''
    @staticmethod
    def build(s):
        if s.startswith('!'): return Negation(), s[1:]
        if s.startswith('^'): return Conjunction(), s[1:]
        if s.startswith('v'): return Disjunction(), s[1:]
        if s.startswith('=>'): return Implication(), s[2:]
        if s.startswith('<=>'): return Equivalence(), s[3:]

class Negation(Connective): pass
class Conjunction(Connective): pass
class Disjunction(Connective): pass
class Implication(Connective): pass
class Equivalence(Connective): pass

class Weight(Token):
    '''
    Base class for representing weights.
    '''
    @staticmethod
    def build(s):
        # If match, build a hard weight.
        if s.startswith('.'): return HardWeight(), s[1:]
        # If s matches a float or integer, build a soft weight.
        number_match = re.match(r'\d+\.?\d*', s)
        if number_match: return SoftWeight(number_match.group(0)), s[len(number_match.group(0)):]

class SoftWeight(Weight):
    def __init__(self, magnitude):
        self._magnitude = magnitude

    @property
    def magnitude(self):
        '''
        Magnitude as a number embedding string.
        '''
        return self._magnitude

class HardWeight(Weight): pass

# Define bracket classes.
class Bracket(Token):
    '''
    Base class representing brackets.
    '''

    @staticmethod
    def build(s):
        if s.startswith('('): return LeftParenthesis(), s[1:]
        if s.startswith(')'): return RightParenthesis(), s[1:]

class LeftParenthesis(Bracket): pass
class RightParenthesis(Bracket): pass

#Define symbol classes.
class Symbol(Token):
    '''
    Base class representing mathematical symbols.
    '''

    @staticmethod
    def build(s):
        if s.startswith('='): return EqualitySign(), s[1:]
        if s.startswith('+'): return PlusSign(), s[1:]
        if s.startswith('-'): return MinusSign(), s[1:]

class EqualitySign(Symbol): pass
class PlusSign(Symbol): pass
class MinusSign(Symbol): pass

# Define comment classes.
class Comment(Token):
    '''
    Base class representing comments.
    '''

    @staticmethod
    def build(s):
        if s.startswith('//'): return LineComment(s), ''

class LineComment(Comment):
    '''
    Base class representing line comments.
    '''

    def __init__(self, s):
        self._text = re.sub(r'//\s*', '', s)

    @property
    def text(self):
        return self._text

# Main.
if __name__ == '__main__':
    sys.argv = ['/home/vishal/Workspace/AffordancePriors_RelationalLearning/TuffyRelationalLearning/AlchemyMLN2TuffyMLN.py',
                   '/home/vishal/Workspace/AffordancePriors_RelationalLearning/TuffyRelationalLearning/SVOPredicateFormula1.mln',
                   '/home/vishal/Workspace/AffordancePriors_RelationalLearning/TuffyRelationalLearning/VOTuples.db',
                   '/home/vishal/Workspace/AffordancePriors_RelationalLearning/TuffyRelationalLearning/learnwts1.mln']
    if len(sys.argv) != 4:
        # The command name.
        cmd_name = sys.argv[0].split('/')[-1].split('\\')[-1]
        # Print usage and exit.
        print >>sys.stderr, "Usage: %s INPUT_MLN_FILENAME INPUT_EVIDENCE_FILENAME OUTPUT_MLN_FILENAME" % cmd_name
        sys.exit(1)

    # Process filenames.
    input_filename = sys.argv[1]
    evidence_filename = sys.argv[2]
    output_filename = sys.argv[3]
    # Parse input file.
    lines = parse_file(input_filename)
    # Parse evidence file.
    evidence_atoms = parse_evidence(evidence_filename)
    # Write output file.
    write_tuffy_network(lines, evidence_atoms, output_filename)