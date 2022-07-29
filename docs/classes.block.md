# class Block

`classes.block.Block(id, tripletList=None, rates=None, dataPath = None)`

A block is a set of observation made in a similar context, which allow to reduce the amount of needed efifciency estimation.

**Parameters**

See object attributes below.

## Class attributes

### `all : dict`
Dictionnary containing blocks id as key and the instance of the blocs as values.

---

## Class methods

No methods in this class

---

## Object attributes

### `id : str`
Unique name of the block (ex: `2013AE`).
### `tripletList : list[Triplet] | None`
List of `Triplet` objects associated to this block.
### `rates : list[Rate] | None`
List of `Rate` objects associated to this block.
### `dataPath : str | None`
Path to the block data.

---

## Object methods

### unload

`unload()`

Unload all the CCD of the block to clear memory.

**Parameters**: None

**Returns**: None

### to_dict

`to_dict()`

Return a dictionary containing all the object information. Useful to save it in a JSON format.

**Parameters**: None

**Returns**:

- `dict`: The containing all the object information.

### to_ai_ready

`to_ai_ready(func = None, vel = 4.5, maxTriplet = 8, maxCCD = 36, randomTriplet = True, randomCCD = True, **kwargs)`

Return a vector that can be used to train the AI.

**Parameters**:

- `func : str` (optional): the type of function for which the parameters will be returned. Must be `tan` for the double tangent form or `square` for the exponential form. You can also precise no function to get both (8 output parameters instead of 4).
- `vel : float`: the volocity for which you want to get the function parameters. The default value correspond to the need of the original data set of used in this project.
- `maxTriplet : int` the minimum number of triplet included in the considered blocks. The default value correspond to the need of the original data set of used in this project. Be careful: if a considered block contain less triplets than this number, the output vectors will don't have the same dimension, which will lead to errors.
- `maxCCD : int`the minimum number of CCD included in the considered triplets. The default value correspond to the need of the original data set of used in this project. Be careful: if a considered triplet contain less CCD than this number, the output vectors will don't have the same dimension, which will lead to errors.
- `randomTriplet : bool` if all blocks doesn't have the same amount of triplet, this parameter allow to select the triplet randomly if it's set to `True`. Otherwise, it will take the first ones.
- `randomCCD : bool` if all triplets doesn't have the same amount of CCD, this parameter allow to select the triplet randomly if it's set to `True`. Otherwise, it will take the first ones.
- `**krags` this parameter is not used. It only allow to quicly adapt a code that contain call to this function on upper classes without having to edit all the parameters.

**Returns**:

- `ndarray`: A Numpy vector containing the input and the output (4 or 8 last elements of the vector).
- `int` The number of elements in the array that compose the output vector.