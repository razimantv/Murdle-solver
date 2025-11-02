from itertools import permutations


class Suspect:
    """Suspects with various attributes."""

    def __init__(self, name, height, hand, eye, hair, zodiac):
        self.data = {
            'name': name,
            'height': height,
            'hand': hand,
            'eye': eye,
            'hair': hair,
            'zodiac': zodiac
        }

    gallery: "dict[str, Suspect]"


# Gallery of suspects
Suspect.gallery = {
    params[0]: Suspect(*params)
    for params in [
        ('Amaranth', (5, 10), 'Right', 'Grey', 'Red', 'Gemini'),
        ('Applegreen', (5, 11), 'Right', 'Blue', 'Bald', 'Libra'),
        ('Aubergine', (5, 2), 'Right', 'Blue', 'Blond', 'Libra'),
        ('Aureolin', (5, 6), 'Left', 'Green', 'Blond', 'Aries'),
        ('Azure', (5, 4), 'Right', 'Brown', 'Brown', 'Gemini'),
        ('Blue', (7, 8), 'Right', 'Blue', 'Blond', 'Gemini'),
        ('Brownstone', (5, 4), 'Left', 'Brown', 'Brown', 'Capricorn'),
        ('Celadon', (5, 6), 'Left', 'Green', 'Brown', 'Leo'),
        ('Champagne', (5, 11), 'Left', 'Hazel', 'Blond', 'Capricorn'),
        ('Coffee', (6, 0), 'Right', 'Brown', 'Bald', 'Sagittarius'),
        ('Copper', (5, 5), 'Right', 'Blue', 'Blond', 'Aries'),
        ('Crimson', (5, 9), 'Left', 'Green', 'Red', 'Aquarius'),
        ('Emerald', (5, 8), 'Left', 'Brown', 'Black', 'Sagittarius'),
        ('Eminence', (5, 2), 'Left', 'Grey', 'Brown', 'Pisces'),
        ('Fuchsia', (5, 8), 'Left', 'Brown', 'Brown', 'Virgo'),
        ('Glaucus', (5, 6), 'Right', 'Brown', 'Brown', 'Virgo'),
        ('Grey', (5, 9), 'Right', 'Brown', 'White', 'Capricorn'),
        ('Honey', (6, 0), 'Left', 'Hazel', 'Brown', 'Scorpio'),
        ('Lapis', (5, 2), 'Right', 'Brown', 'Brown', 'Cancer'),
        ('Lavender', (5, 9), 'Right', 'Green', 'Grey', 'Virgo'),
        ('Mango', (5, 10), 'Left', 'Brown', 'Bald', 'Taurus'),
        ('Maroon', (6, 2), 'Right', 'Hazel', 'Red', 'Scorpio'),
        ('Mauve', (5, 8), 'Right', 'Brown', 'Black', 'Taurus'),
        ('Midnight', (5, 8), 'Left', 'Blue', 'Brown', 'Sagittarius'),
        ('Navy', (5, 9), 'Right', 'Blue', 'Brown', 'Cancer'),
        ('Obsidian', (5, 4), 'Left', 'Green', 'Black', 'Leo'),
        ('Pine', (5, 6), 'Right', 'Brown', 'Black', 'Taurus'),
        ('Raspberry', (6, 0), 'Left', 'Blue', 'Blond', 'Aries'),
        ('Red', (6, 2), 'Left', 'Brown', 'Brown', 'Aries'),
        ('Rose', (5, 7), 'Left', 'Brown', 'Brown', 'Scorpio'),
        ('Ruby', (5, 6), 'Right', 'Green', 'Red', 'Libra'),
        ('Rulean', (5, 8), 'Right', 'Blue', 'Red', 'Leo'),
        ('Saffron', (5, 2), 'Left', 'Hazel', 'Blond', 'Libra'),
        ('Silverton', (6, 4), 'Right', 'Blue', 'Silver', 'Leo'),
        ('Slate', (5, 5), 'Left', 'Brown', 'Brown', 'Aquarius'),
        ('Tangerine', (5, 5), 'Left', 'Hazel', 'Blond', 'Pisces'),
        ('Tuscany', (5, 5), 'Left', 'Green', 'Grey', 'Libra'),
        ('Verdigris', (5, 3), 'Left', 'Blue', 'Grey', 'Leo'),
        ('Vermillion', (5, 9), 'Left', 'Grey', 'White', 'Pisces'),
        ('Violet', (5, 0), 'Right', 'Blue', 'Blond', 'Virgo'),
    ]
}


class Puzzle:
    """Main puzzle class
    Initialise with subjects (suspects and fields like weapon, location, etc.)
    and clues. Solve with the solve() method."""

    def __init__(self, subjects, clues, specialclue=None):
        self.suspects = [
            Suspect.gallery[suspect] for suspect in subjects['suspect']
        ]

        # Assign ids to non-suspect fields and store them separately
        self.fields = [k for k in subjects if k != 'suspect']
        self.field_id = {field: i for i, field in enumerate(self.fields)}
        self.field_values = {field: subjects[field] for field in self.fields}
        self.clues = clues
        self.specialclue = specialclue

        # Precompute all permutations and their inverses
        self.perms = list(permutations(list(range(len(self.suspects)))))
        self.invperms = [self._inverse_permutation(
            perm) for perm in self.perms]
        self.N_perms = len(self.perms)

    def _update_perm_indices(self, perm_indices):
        """Update permutation indices in a manner similar to base-N
        counting."""
        for i in range(len(self.fields)):
            perm_indices[i] += 1
            if perm_indices[i] == self.N_perms:
                perm_indices[i] = 0
            else:
                return True
        return False

    @staticmethod
    def _inverse_permutation(perm):
        """Invert a permutation for inverse mapping"""
        ret = [0] * len(perm)
        for i, x in enumerate(perm):
            ret[x] = i
        return ret

    @staticmethod
    def _suspect_idx_with_field(
        field, value, field_id, field_values, inverse_permutations
    ):
        """Get the suspect index with a given field value"""
        field_idx = next(
            i for i, x in enumerate(field_values[field]) if x == value
        )
        return inverse_permutations[field_id[field]][field_idx]

    def solve(self):
        """Solve the puzzle, returning the culprit and their attributes."""
        perm_indices = [0] * len(self.fields)
        while True:
            # Loop through all permutations
            forward_permutations = [self.perms[idx] for idx in perm_indices]
            inverse_permutations = [self.invperms[idx] for idx in perm_indices]

            # If all clues are true, we found a solution
            if all(
                clue.true(
                    self.suspects, self.field_id, self.field_values,
                    forward_permutations, inverse_permutations
                )
                for clue in self.clues
            ):
                break
            elif not self._update_perm_indices(perm_indices):
                return None

        if self.specialclue is None:
            # If there is no special clue, there should be a liar
            # Find the liar and their index
            liarclue = next(x for x in self.clues if type(x) is Clue_Liar)
            suspect = liarclue.liar(
                self.suspects, self.field_id, self.field_values,
                forward_permutations, inverse_permutations
            )
            suspect_idx = next(
                i for i, x in enumerate(self.suspects)
                if x.data['name'] == suspect
            )
        else:
            # Otherwise, use the special clue to find the culprit
            suspect_idx = self._suspect_idx_with_field(
                *self.specialclue, self.field_id, self.field_values,
                inverse_permutations
            )

        # Return the culprit's name and attributes
        return self.suspects[suspect_idx].data['name'], *[
            self.field_values[k][perm[suspect_idx]]
            for k, perm in zip(self.fields, forward_permutations)
        ]


class Clue:
    """A clue of the form: If field1 is value1, then field2 is value2.
    field1 and field2 can be one of the non-suspect fields.
    Only field2 can be a suspect attribute like name, height, etc.
    """

    def __init__(self, field1, value1, field2, value2):
        self.field1 = field1
        self.value1 = value1
        self.field2 = field2
        self.value2 = value2

    def true(self, suspects, field_id, field_values, fwperm, invperm):
        """Check if the clue is true given the current permutations."""
        suspect_idx = Puzzle._suspect_idx_with_field(
            self.field1, self.value1, field_id, field_values, invperm
        )
        if self.field2 in field_id:
            field2_idx = fwperm[field_id[self.field2]][suspect_idx]
            return field_values[self.field2][field2_idx] == self.value2
        else:
            return suspects[suspect_idx].data[self.field2] == self.value2


class Clue_Not(Clue):
    """Negated clue"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def true(self, *args, **kwargs):
        return not super().true(*args, **kwargs)


class Clue_Oneof:
    """One of several clues is true."""

    def __init__(self, clues):
        self.clues = [Clue(*clue) for clue in clues]

    def true(self, *args, **kwargs):
        return sum(clue.true(*args, **kwargs) for clue in self.clues) == 1


class Clue_Group(Clue_Oneof):
    """One of group of values for field1 correspond to value2 for field2."""

    def __init__(self, field1, values1, field2, value2):
        super().__init__([
            [field1, value1, field2, value2] for value1 in values1
        ])


class Clue_Liar:
    """Exactly one suspect is lying."""

    def __init__(self, statements):
        self.suspects = statements.keys()
        self.clues = statements.values()

    def truths(self, *args, **kwargs):
        """Get the truth values for all suspects' statements."""
        return [clue.true(*args, **kwargs) for clue in self.clues]

    def true(self, *args, **kwargs):
        return sum(self.truths(*args, **kwargs)) == (len(self.clues) - 1)

    def liar(self, *args, **kwargs):
        """Get the name of the suspect who is lying."""
        return next(
            suspect for suspect, truth in zip(
                self.suspects, self.truths(*args, **kwargs)
            ) if not truth
        )
