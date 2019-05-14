from __future__ import print_function
import argparse

class Dhondt(object):
    def __init__(self, parties_and_votes, total_seats):
        self.parties_and_votes = parties_and_votes
        self.allocated_seats = { k:0 for (k,v) in parties_and_votes.items() }
        self.total_seats = total_seats

    def _quotient(self, votes, seats):
        return float(votes) / (seats + 1)

    def __call__(self):
        for i in range(self.total_seats):
            highest_quotient = (None, 0)
            for party, seats in self.allocated_seats.items():
                quot = self._quotient(self.parties_and_votes[party], seats)
                if quot > highest_quotient[1]:
                    highest_quotient = (party, quot)

            self.allocated_seats[highest_quotient[0]] += 1

        return self.allocated_seats

def parse_and_validate(parties):
    """Returns success, parsed list. If the format is invalid, success = False"""
    parties_and_votes = {}
    for party in parties:
        if party[0].isdigit():
            print(party[0])
            return False, parties_and_votes
        if not party[1].isdigit():
            print(party[1])
            return False, parties_and_votes
        parties_and_votes[party[0]] = int(party[1])

    return True, parties_and_votes
            

if __name__ == '__main__':
    # p_and_v = {'green' : 2037, 'blue' : 1524, 'red' : 6123, 'yellow' : 1421, 'orange' : 3000}
    parser = argparse.ArgumentParser(description="Calculate proportional representation based on election results")
    parser.add_argument('--seats', '-s', type=int, dest='seats')
    parser.add_argument('--parties', '-p', nargs=2, dest="p_and_v_unparsed", action='append', help='list of the form "party count party count.."')
    args = parser.parse_args()

    success, p_and_v = parse_and_validate(args.p_and_v_unparsed)
    if not success:
        parser.print_help()
        exit(1)

    for k,v in Dhondt(p_and_v, args.seats)().items():
        print(k,': ',v)
