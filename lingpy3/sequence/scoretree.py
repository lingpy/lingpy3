# coding: utf8
from __future__ import unicode_literals, print_function, division

import networkx

from lingpy3.util import multicombinations2, uniq
from lingpy3.algorithm import ScoreDict


class ScoreTree(networkx.DiGraph):
    def __init__(self, spec):
        """
        Function imports score trees for a given range of sound classes and
        converts them into a graph.
        """
        networkx.DiGraph.__init__(self)
        for key, values in spec:
            self.add_node(key, val=values[0])
            for value in values[1:]:
                value = value.strip()
                if value != '-':
                    node, weight = value.split(':')
                    self.add_edge(key, node, weight=int(weight))

    @staticmethod
    def _find_all_paths(graph, start, end, path=[]):
        """
        Function returns all paths which connect two nodes in a network.
        """
        assert start in graph.node and end in graph.node
        path = path + [start]
        if start == end:
            return [path]
        paths = []
        for node in graph.edge[start].keys():
            if node not in path:
                newpaths = ScoreTree._find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def _find_dir_path(self, start, end):
        """
        Function finds the path connecting two nodes in a directed graph under the
        condition that the two nodes are connected either directly or by a common
        ancestor node.
        """
        # first possibility: there is a direct path between the two nodes
        try:
            return networkx.shortest_path(self, start, end)
        except networkx.NetworkXNoPath:
            pass

        # second possibility: there is a direct path between the two nodes, but
        # it starts from the other node
        try:
            return networkx.shortest_path(self, end, start)
        except networkx.NetworkXNoPath:
            pass

        # third possibility: there is no direct path between the nodes in
        # neither direction, but there is a path in an undirected graph
        paths = ScoreTree._find_all_paths(self.to_undirected(), start, end)
        if paths:
            # here, we simply check, whether within all paths connecting the
            # two nodes there is a node which directly connects to both nodes
            # (i.e. which is the ancestor of both nodes). If this is the case,
            # the respective shortest path is what we are looking for.
            current_path_length = max([len(path) for path in paths])
            shortest_paths = networkx.shortest_path(self)
            current_path = []
            for path in paths:
                for node in path[1:-1]:
                    if start in shortest_paths[node].keys() \
                            and end in shortest_paths[node].keys():
                        if len(path) <= current_path_length:
                            current_path_length = len(path)
                            current_path = path
                            break
            return current_path or False

        # fourth condition: there is no path connecting the nodes at all
        return False

    def _get_path_length(self, path):
        """
        Function returns the length of a path in a weighted graph.
        """
        if path is False:
            return False
        undirected = self.to_undirected()
        return sum([undirected[n1][n2]['weight'] for n1, n2 in zip(path[:-1], path[1:])])

    def _get_starting_value(self, node1, node2, max_, default):
        distance = self._get_path_length(self._find_dir_path(node1, node2))
        # make sure that the distance doesn't exceed the default value.
        if distance is False or distance > max_:
            return default
        return max_ + default - distance

    def get_scoredict(self):
        """
        Function creates a scoring dictionary for individually defined sound
        classes and individually created scoring trees by counting the path length
        connecting all nodes and assigning different start weights for vowels and
        consonants.
        """
        score_dict = {}

        # iterate over all nodes in the previously created self of sound class
        # transitions
        for node1, node2 in multicombinations2(self.nodes()):
            # if the nodes are the same, assign them the values for vowel-vowel or
            # consonant-consonant identity these values might be made changeable in
            # later versions
            if node1 == node2:
                # for vowels and glides, the same starting value is assumed
                if self.node[node1]['val'] in ['v', 'g']:
                    value = 5
                # make sure, that tones do not score
                elif self.node[node1]['val'] == 't':
                    value = 2
                else:
                    value = 10
            # if the nodes are different, see, if there is a connection
            # between them defined in the directed network
            else:
                # treat vowel-vowel and consonant-consonant matches
                # differently
                if self.node[node1]['val'] == self.node[node2]['val']:
                    # for vowels and glides, the starting value to subtract the
                    # weighted pathlength from is the vowel-vowel-identity
                    # score
                    if self.node[node1]['val'] in ['v', 'g']:
                        # make sure that the distance doesn't exceed the
                        # default value for vowel-vowel matches, which
                        # should be zero, if there is no connection in the
                        # path defined
                        value = self._get_starting_value(node1, node2, 5, 0)

                    # for consonants, the starting value is the
                    # consonant-consonant score
                    elif self.node[node1]['val'] == 'c':
                        # make sure that the minimum value of C-C-matches is zero
                        value = self._get_starting_value(node1, node2, 10, 0)
                    else:
                        # make sure that tone-tone classes score with zero
                        value = 1
                # for vowel-consonant, vowel-glide and glide-consonant
                # matches, the starting value is the vowel-vowel score (may
                # also be changed in later versions)
                else:
                    choices = [self.node[node1]['val'], self.node[node2]['val']]

                    # make sure to exclude tones from all matchings in
                    # order to force the algorithm to align tones with
                    # tones or gaps and with nothing else
                    if 't' in choices:
                        value = -20
                    # matches of glides with different classes
                    elif 'g' in choices:
                        # glides and vowels or glides and consonants
                        if 'v' in choices or 'c' in choices:
                            value = self._get_starting_value(node1, node2, 10, -5)
                        else:
                            raise ValueError  # pragma: no cover
                    else:
                        value = self._get_starting_value(node1, node2, 15, -10)

            score_dict[(node2, node1)] = score_dict[(node1, node2)] = value

        # add the characters for gaps in the multiple alignment process
        # note that gaps and gaps should be scored by zero according to Feng &
        # Doolittle. so far I have scored them as -1, and scoring gaps as zero made
        # the alignments getting worse, probably because most tests have been based
        # on profiles. we probably need a very good gap score.
        for node in self.nodes():
            # missing data
            score_dict[('0', node)] = score_dict[(node, '0')] = 0

            # swaps
            score_dict[('+', node)] = score_dict[(node, '+')] = -100

            # specific values
            score_dict[('X', node)] = score_dict[(node, 'X')] = 0

        score_dict[('+', 'X')] = score_dict[('X', '+')] = -5
        score_dict[('+', '+')] = 0
        score_dict[('0', '0')] = 0
        score_dict[('X', '0')] = score_dict[('0', 'X')] = 0

        # define the gaps
        score_dict[('X', 'X')] = 0

        chars = uniq([s[0] for s in score_dict.keys()])
        matrix = [[0 for _ in range(len(chars))] for _ in range(len(chars))]
        for (i, charA), (j, charB) in multicombinations2(enumerate(chars)):
            if i < j:
                matrix[i][j] = score_dict.get((charA, charB), -100)
                matrix[j][i] = score_dict.get((charB, charA), -100)
            elif i == j:
                matrix[i][j] = score_dict[charA, charB]

        return ScoreDict(chars, matrix)
