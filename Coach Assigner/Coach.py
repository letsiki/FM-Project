class Coach:
    def __init__(self, *, name, Dis, Det, Mot, Tec, Tac, Att, Def, Men):
        # Initialize cache
        self._cache = {
            'ATe': None,
            'ATa': None,
            'DTe': None,
            'DTa': None,
            'PTe': None,
            'PTa': None
        }
        
        self.name = name
        self.Dis = Dis  # Discipline
        self.Det = Det  # Determination
        self.Mot = Mot  # Motivating
        self.Tec = Tec  # Technique
        self.Tac = Tac  # Tactical
        self.Att = Att  # Attacking
        self.Def = Def  # Defending
        self.Men = Men  # Mental

    # Properties to calculate once, unless attributes change
    @property
    def ATe(self):
        if self._cache['ATe'] is None:
            self._cache['ATe'] = self.calculate_ATe()
        return self._cache['ATe']

    @property
    def ATa(self):
        if self._cache['ATa'] is None:
            self._cache['ATa'] = self.calculate_ATa()
        return self._cache['ATa']

    @property
    def DTe(self):
        if self._cache['DTe'] is None:
            self._cache['DTe'] = self.calculate_DTe()
        return self._cache['DTe']

    @property
    def DTa(self):
        if self._cache['DTa'] is None:
            self._cache['DTa'] = self.calculate_DTa()
        return self._cache['DTa']

    @property
    def PTe(self):
        if self._cache['PTe'] is None:
            self._cache['PTe'] = self.calculate_PTe()
        return self._cache['PTe']

    @property
    def PTa(self):
        if self._cache['PTa'] is None:
            self._cache['PTa'] = self.calculate_PTa()
        return self._cache['PTa']

    # Conversion method: Converts internal score to stars
    def convert_score_to_rating(self, score):
        if score >= 271:
            stars = 5.0
        elif score >= 241:
            stars = 4.5
        elif score >= 211:
            stars = 4.0
        elif score >= 181:
            stars = 3.5
        elif score >= 151:
            stars = 3.0
        elif score >= 121:
            stars = 2.5
        elif score >= 91:
            stars = 2.0
        elif score >= 61:
            stars = 1.5
        elif score >= 31:
            stars = 1.0
        else:
            stars = 0.5

 
        return stars

    # Calculation methods using FM24 formulas and converting the score to star rating
    def calculate_ATe(self):
        score = ((self.Att * 6) + (self.Tec * 3) + ((self.Mot + self.Det + self.Dis) * 2)) # Convert to 0-300 scale
        return self.convert_score_to_rating(score)

    def calculate_ATa(self):
        score = ((self.Att * 6) + (self.Tac * 3) + ((self.Mot + self.Det + self.Dis) * 2)) # Convert to 0-300 scale
        return self.convert_score_to_rating(score)

    def calculate_DTe(self):
        score = ((self.Def * 6) + (self.Tec * 3) + ((self.Mot + self.Det + self.Dis) * 2)) # Convert to 0-300 scale
        return self.convert_score_to_rating(score)

    def calculate_DTa(self):
        score = ((self.Def * 6) + (self.Tac * 3) + ((self.Mot + self.Det + self.Dis) * 2)) # Convert to 0-300 scale
        return self.convert_score_to_rating(score)

    def calculate_PTe(self):
        score = ((self.Men * 6) + (self.Tec * 3) + ((self.Mot + self.Det + self.Dis) * 2)) # Convert to 0-300 scale
        return self.convert_score_to_rating(score)

    def calculate_PTa(self):
        score = ((self.Men * 6) + (self.Tac * 3) + ((self.Mot + self.Det + self.Dis) * 2)) # Convert to 0-300 scale
        return self.convert_score_to_rating(score)

    # Method to get a list of the best roles based on ratings
    def best_roles(self):
        roles = [
            ('ATe', self.ATe),
            ('ATa', self.ATa),
            ('DTe', self.DTe),
            ('DTa', self.DTa),
            ('PTe', self.PTe),
            ('PTa', self.PTa)
        ]

        # Get maximum rating to compare with
        max_rating = max(rating for _, rating in roles)

        # Return roles with ratings within 2 units of the maximum rating
        return [(role, rating) for role, rating in roles if rating >= max_rating - 0.5]

    # Method to invalidate cache if attributes change
    def _invalidate_cache(self):
        self._cache = {key: None for key in self._cache.keys()}

    # Setter methods to invalidate cache when attributes change
    @property
    def Dis(self):
        return self._Dis

    @Dis.setter
    def Dis(self, value):
        self._Dis = value
        self._invalidate_cache()

    @property
    def Det(self):
        return self._Det

    @Det.setter
    def Det(self, value):
        self._Det = value
        self._invalidate_cache()

    @property
    def Mot(self):
        return self._Mot

    @Mot.setter
    def Mot(self, value):
        self._Mot = value
        self._invalidate_cache()

    @property
    def Tec(self):
        return self._Tec

    @Tec.setter
    def Tec(self, value):
        self._Tec = value
        self._invalidate_cache()

    @property
    def Tac(self):
        return self._Tac

    @Tac.setter
    def Tac(self, value):
        self._Tac = value
        self._invalidate_cache()

    @property
    def Att(self):
        return self._Att

    @Att.setter
    def Att(self, value):
        self._Att = value
        self._invalidate_cache()

    @property
    def Def(self):
        return self._Def

    @Def.setter
    def Def(self, value):
        self._Def = value
        self._invalidate_cache()

    @property
    def Men(self):
        return self._Men

    @Men.setter
    def Men(self, value):
        self._Men = value
        self._invalidate_cache()

if __name__ == '__main__':
    Ravn = Coach(name='Ravn', Dis=15, Det=12, Mot=20, Tec=18, Tac=13, Att=16, Def=11, Men=14)
    # print(Ravn.convert_score_to_rating(Ravn.calculate_PTa()))
    print(Ravn.calculate_ATe())