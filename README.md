# Murdle-solver
Find the solution to the puzzles at [murdle.com](https://murdle.com).

# Usage

See [example](Example.ipynb) for usage details.

The puzzle needs to be created with subjects, clues, and perhaps a special clue.

## Subjects

These are suspects, weapons and locations (and in some puzzles, motives). They need to be set up as a dictionary of lists.

```python
subjects = {
    'suspect': ['Tangerine', 'Brownstone', 'Pine', 'Verdigris', 'Coffee'],
    'weapon': ['Coffee', 'Brick', 'Knife', 'Straw', 'Pot'],
    'location': ['Bathroom', 'Parking', 'Bean Room', 'Counter', 'Courtyard']
}
```

There can be any number of categories as keys, but each category must have the same number of elements. Only the names of the suspects need to be provided. Their attributes (eye color, height etc.) will be found from the database.

## Clues

Clues can be of different types.

A normal `Clue` is of the form `field1, value1, field2, value1` meaning that the subject with `field1` equal to `value1` has `field2` equal to `value2`. `field1` needs to be a non-person attribute such as weapon or location. `field2` can be a personal attribute (name/eye/height/zodiac/hair) or a non-person attribute.

```python
Clue('location', 'Bathroom', 'name', 'Tangerine')
```

A negated clue, such that `field1` equal to `value1` does NOT have `field2` equal to `value2`, can be created with `Clue_Not`.

```python
Clue_Not('location', 'Bathroom', 'name', 'Tangerine')
```

A clue group is a set of clues that say that exactly one of the given values of `field1` has `field2` equal to `value2`. This can be created with `Clue_Group`.

```python
Clue_Group('weapon', ['Brick', 'Straw', 'Pot'], 'name', 'Brownstone')
```

It is also possible to specify that exactly one of a set of clues is true, through `Clue_Oneof`.

```python
Clue_Oneof([
    ['location', 'Bean Room', 'weapon', 'Straw'],
    ['weapon', 'Pot', 'name', 'Tangerine']
])
```

Finally, some puzzles have a set of statements from suspects such that exactly one of them, the murderer, is lying. This can be set up using `Clue_Liar` with a dictionary of suspect names mapped to their statements expressed as clues.

```python
Clue_Liar({
    'Mauve': Clue('location', 'Courts', 'name', 'Rose'),
    'Rose': Clue('weapon', 'Pipe', 'name', 'Rose'),
    'Aubergine': Clue_Not('weapon', 'Pipe', 'name', 'Mauve'),
    'Azure': Clue('weapon', 'Pipe', 'name', 'Rose')
})
```

The puzzle requires all the clues need to be in a list.

## Special clue

In puzzles without a set of statements to pick the murderer from the liar, there is also a special clue specifying the location/weapon/motive of the murderer. This can be set up as 

```python
special_clue = ['weapon', 'Cube']
```

## Puzzle

The puzzle is set up using the subjects, clues, and the special clue if it exists.

```python
puzzle = Puzzle(subjects, clues, specialclue)
```

It can be then solved using

```python
puzzle.solve()
```

`solve()` returns the name and other categories of the murderer.
