# `classes.block.Block`

## Class attributes

- `all`: dictionnary containing blocks id as key and the instance of the blocs as values.

---

## Class methods

No methods in this class

---

## Object attributes

- `id : str`: unique name of the block (ex: `2013AE`).
- `tripletList : list[Triplet]` (optional): list of `Triplet` objects associated to this block.
- `rates : list[Rate]` (optional): list of `Rate` objects associated to this block.
- `dataPath : str` (optional): path to the block data.

---

## Object methods

### `unload(self)`

Delete the object and all associated triplets to clear memory.

**inputs**:
- `self : Block`: instance of the `block` object you want to unload.

**Returns**: None

### `to_dict(self)`

Return a dictionary containing all the object informations. Useful to save it in a JSON or YAML format.

**inputs**:
- `self : Block`: instance of the `block` object you want to get as dictionary.

**Returns**:
- `dict`: The containing all the object informations

### `to_ai_ready(self)`

Return a vector that can be used to train the AI.

**inputs**:
- `self : Block`: instance of the `block` object you want to get as vector.
- `func : str = None` (optional): the type of function for which the parameters will be returned. Must be `tan` for the double tangent form or `square` for the exponential form. You can also precise no function to get both (8 output parameters instead of 4).
- `vel : float = 4.5`: the volocity for which you want to get the function parameters. The default value correspond to the need of the original data set of used in this project.
- `maxTriplet : int = 8` the minimum number of triplet included in the considered blocks. The default value correspond to the need of the original data set of used in this project. Be careful: if a considered block contain less triplets than this number, the output vectors will don't have the same dimension, which will lead to errors.
- `maxCCD : int = 36`the minimum number of CCD included in the considered triplets. The default value correspond to the need of the original data set of used in this project. Be careful: if a considered triplet contain less CCD than this number, the output vectors will don't have the same dimension, which will lead to errors.
- `randomTriplet : bool = True` if all blocks doesn't have the same amount of triplet, this parameter allow to select the triplet randomly if it's set to `True`. Otherwise, it will take the first ones.
- - `randomCCD : bool = True` if all triplets doesn't have the same amount of CCD, this parameter allow to select the triplet randomly if it's set to `True`. Otherwise, it will take the first ones.

**Returns**:
- `ndarray`: A Numpy vector containing the input and the output (4 or 8 last elements of the vector)