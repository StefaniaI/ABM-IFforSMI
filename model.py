import numpy as np
import copy

debug = False


class User:
    def __init__(self, config, id):
        self.config = config
        self.id = id

        # the best CC followed so far
        self.best_followed_CC = None

    def decide_follow(self, c):
        '''Evaluates whether the user wants to follow CC c.

        input: c - a content creator
        ------
        output: bool - decision if it follows c'''

        # it follows c iff they are better (closer to top) then the best followed so far
        if (self.best_followed_CC is None) or (self.best_followed_CC.id > c.id):
            self.best_followed_CC = c
            return True

        return False


class CC:
    def __init__(self, config, id):
        self.config = config
        self.id = id


class Network:
    '''Class capturing a follower network between from users to items.
    In this version of the code we assumme that each item is a content creator/channel.
    '''

    def __init__(self, config, G=None, favorite=None):
        self.config = config

        num_users = config['num_users']
        num_CCs = config['num_CCs']

        self.G = G
        if self.G is None:
            self.G = np.zeros((num_users, num_CCs), dtype=bool)

        # self.favorite = favorite

        self.num_followers = np.count_nonzero(self.G, axis=0)
        self.num_followees = np.count_nonzero(self.G, axis=1)

    def follow(self, u, c, num_timestep, when_users_found_best):
        '''User u follows content creator c; and updates the Network

        input: u - user
               c - CC
               num_timestep - the iteration number of the platform (int)
               when_users_found_best - a list of length the number of users who keeps the timesteps when each of the user found their best CC (or -1 if they didn't yet)
        '''

        if not self.G[u.id][c.id]:
            if u.decide_follow(c):
                self.G[u.id][c.id] = True
                self.num_followers[c.id] += 1
                self.num_followees[u.id] += 1

                # if c is the top CC, then u found their best CC this round
                if c.id == 0:
                    when_users_found_best[u.id] = num_timestep
                if debug:
                    print("       ", num_timestep, ": " ,u.id, " folllows ", c.id,
                          ", when_users_found_best becomes ", when_users_found_best,
                          ", and num_followers is ", self.num_followers)
                    # input()

    def is_following(self, u, c):
        return self.G[u.id][c.id]


class RS:
    '''Class for the Recommender System (i.e., descoverability  procedure).
    '''

    def __init__(self, config, content_creators):
        self.config = config

    def recommend_general(self, content_creators, num_followers):
        ''' input: content_creators - a list of content creators
                   num_followers - a numpyarray with the probability of choosing each CC
        -----
        output: a CC chosen based on PA'''

        num_users = self.config['num_users']
        num_CCs = self.config['num_CCs']
        alpha = self.config['alpha']

        prob_choice = (num_followers + np.ones(num_CCs))**alpha
        prob_choice /= sum(prob_choice)
        if debug:
            print('Prob choice RS:', prob_choice)

        return self.config['random_generator'].choice(content_creators, num_users, p=prob_choice)

    def recommend_random(self, content_creators):
        ''' input: content_creators - a list of content creators
        -----
        output: a list of recommendations of CC chosen uniformly at ranodm'''

        num_users = self.config['num_users']
        return self.config['random_generator'].choice(content_creators, num_users)

    def recommend_PA(self, content_creators, num_followers):
        ''' input: content_creators - a list of content creators
                   num_followers - a numpyarray with the probability of choosing each CC
        -----
        output: a CC chosen based on PA'''

        num_users = self.config['num_users']
        num_CCs = self.config['num_CCs']
        prob_choice = num_followers + np.ones(num_CCs)
        prob_choice /= sum(prob_choice)
        if debug:
            print('Prob choice RS:', prob_choice)
        return self.config['random_generator'].choice(content_creators, num_users, p=prob_choice)

    def recommendable_Extreme(self, content_creators, num_followers, for_PA=True):
        ''' input: content_creators - a list of content creators
                   num_followers - a numpyarray with the probability of choosing each CC
                   for_PA - is True if we do ExtremePA and false if we do ExtremeAntiPA
        -----
        output: the CCs that have a maximum number of followers'''

        extreme_num_followers = max(
            num_followers) if for_PA else min(num_followers)

        most_popular_CCs = []  # or least_popular if for_PA = False
        for c in content_creators:
            if num_followers[c.id] == extreme_num_followers:
                most_popular_CCs.append(c)

        return most_popular_CCs

    def recommend_Extreme(self, content_creators, num_followers, for_PA=True):
        ''' input: content_creators - a list of content creators
                   num_followers - a numpyarray with the probability of choosing each CC
                   for_PA - is True if we do ExtremePA and false if we do ExtremeAntiPA
        -----
        output: a CC chosen based on Extreme PA'''

        num_users = self.config['num_users']

        most_popular_CCs = self.recommendable_Extreme(
            content_creators, num_followers, for_PA)
        return self.config['random_generator'].choice(most_popular_CCs, num_users)

    def recommend_AntiPA(self, content_creators, num_followers):
        ''' input: content_creators - a list of content creators
                   num_followers - a numpyarray with the probability of choosing each CC
        -----
        output: a CC chosen based on Anti-PA (nodes proportional to exp(-deg) )'''

        num_users = self.config['num_users']
        num_CCs = self.config['num_CCs']
        # prob_choice = np.exp(-num_followers) / sum(np.exp(-num_followers))
        prob_choice = (num_followers + np.ones(num_CCs))**(-1)
        prob_choice /= sum(prob_choice)

        return self.config['random_generator'].choice(content_creators, num_users, p=prob_choice)

    def recommend(self, content_creators, num_followers):
        '''A rapper that choses the appropriate RS.

        input: content_creators - a list of content creators
               num_followers - a numpyarray with the probability of choosing each CC
        -----
        output: a list of reccommendations (one per user)'''

        if self.config['rs_model'] == 'UR':
            return self.recommend_random(content_creators)
        elif self.config['rs_model'] == 'PA':
            return self.recommend_PA(content_creators, num_followers)
        elif self.config['rs_model'] == 'general':
            return self.recommend_general(content_creators, num_followers)
        elif self.config['rs_model'] == 'ExtremePA':
            return self.recommend_Extreme(content_creators, num_followers, for_PA=True)
        elif self.config['rs_model'] == 'ExtremeAntiPA':
            return self.recommend_Extreme(content_creators, num_followers, for_PA=False)
        elif self.config['rs_model'] == 'AntiPA':
            return self.recommend_AntiPA(content_creators, num_followers)
        elif self.config['rs_model'] == 'PA-AntiPA':
            if self.config['random_generator'].random() < 0.5:
                return self.recommend_PA(content_creators, num_followers)
            return self.recommend_AntiPA(content_creators, num_followers)


class Platform:
    def __init__(self, config):
        self.config = config

        # the platform keeps track of the number of timesteps it has been iterated
        self.timestep = 0

        self.network = Network(config)
        self.users = [User(config, i)
                      for i in range(config['num_users'])]
        self.CCs = [CC(config, i)
                    for i in range(config['num_CCs'])]
        self.RS = RS(config, self.CCs)

        # keep track of the timesteps when users found their best CC
        self.users_found_best = [-1 for u in self.users]
        # keep track of the position of the recommended CC in the ranking of the user
        # self.users_rec_pos = []
        # keep track of the average quality experienced by users
        self.average_pos_best_CC = []

        # the users who did not converged yet
        self.id_searching_users = list(range(self.config['num_users']))

        if debug:
            print('Generated users and CCs.')

    def iterate(self):
        '''Makes one iteration of the platform.
        Used only to update the state of the platform'''

        # 0) the platform starts the next iteration
        self.timestep += 1

        # 1) each user gets a recommendation
        recs = self.RS.recommend(self.CCs, self.network.num_followers)
        # record the position of the recommended CC
        # self.users_rec_pos.append([c.id for i, c in enumerate(recs)])

        # 2) each user decides whether or not to follow the recommended CC
        for u in self.users:
            self.network.follow(
                u, recs[u.id], self.timestep, self.users_found_best)

        # 3) if we run until convergence, update the searching users
        if self.config['num_steps'] == 0:
            self.update_searching_users()

        # record the average CC position experienced by CCs
        average_pos = 0
        num_users = self.config['num_users']
        for u in self.users:
            average_pos += u.best_followed_CC.id / num_users
        self.average_pos_best_CC.append(average_pos)

        if debug:
            print('Recommendations: ', [r.id for r in recs])
            print('New network:', self.network.G)
            print('Number of followers:', self.network.num_followers)
            print('Number of followees:', self.network.num_followees)

    def update_searching_users(self):
        '''Updates the list of users who are still searching for the best CC.
        i.e. those who did not find the best CC out of the ones that could be recommended
        '''

        if 'Extreme' in self.config['rs_model']:
            # under non-exploratory RSs, the searching users are only the ones who can still find somebody better

            # 1) get the CCs with a maximum number of followers
            for_PA = True if self.config['rs_model'] == 'ExtremePA' else False
            most_popular_CCs = self.RS.recommendable_Extreme(
                self.CCs, self.network.num_followers, for_PA)

            # 2) find if the user with id i converged
            def not_converged(i):
                u = self.users[i]
                for c in most_popular_CCs:
                    if c.id < u.best_followed_CC.id:
                        return True
                return False

            # 3) filter users based on whether they can still find a better CC
            self.id_searching_users = list(
                filter(not_converged, self.id_searching_users))
        else:
            # under exploratory RSs, the searching users are only the ones who did not find the best
            self.id_searching_users = list(
                filter(lambda i: self.users[i].best_followed_CC.id != 0, self.id_searching_users))

    def check_convergence(self):
        # the platform converged if there are no more searching users (users who can find better CCs)
        return len(self.id_searching_users) == 0
