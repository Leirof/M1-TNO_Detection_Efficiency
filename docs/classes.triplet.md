# class Triplet

`classes.triplet.Triplet(id, tripletList=None, rates=None, dataPath = None)`

A triplet is a set of 3 observation of the same portion of the sky, made at 3 different moments (usually distant from 1 hour). These 3 observation allow to detect moving objects by comparing object position over the 3 images.

**Parameters**

See object attributes below.

## Class attributes

### `all : dict`
Dictionnary containing triplets id as key and the instance of the triplet as values.

---

## Class methods

No methods in this class

---

## Object attributes

### `id : str`
Unique name of the triplet (ex: `2013AE+0+1`).
### `shottList : list[shot] | None`
List of `Shot` objects associated to this triplet.
### `block : Block | None`
Parent block of this triplet.
### `rates : list[Rate] | None`
List of `Rate` objects associated to this block.
### `dataPath : str | None`
Path to the block data.

---

## Object methods

### unload

`unload()`

Unload all the CCD of the triplet to clear memory.

**Parameters**: None

**Returns**: None

### to_dict

`to_dict()`

Return a dictionary containing all the object information. Useful to save it in a JSON format.

**Parameters**: None

**Returns**:

- `dict`: The containing all the object information.

### to_ai_ready

`to_ai_ready(withrate=True, func=None, vel=4.5, maxCCD=36, randomCCD=True, **kwargs)`

Return a vector that can be used to train the AI.

**Parameters**:

- `whitrate : bool` set to tru if the function return the detection rate at the end of the vector.
- `func : str` (optional): the type of function for which the parameters will be returned. Must be `tan` for the double tangent form or `square` for the exponential form. You can also precise no function to get both (8 output parameters instead of 4).
- `vel : float`: the volocity for which you want to get the function parameters. The default value correspond to the need of the original data set of used in this project.
- `maxCCD : int`the minimum number of CCD included in the considered triplets. The default value correspond to the need of the original data set of used in this project. Be careful: if a considered triplet contain less CCD than this number, the output vectors will don't have the same dimension, which will lead to errors.
- `randomCCD : bool` if all triplets doesn't have the same amount of CCD, this parameter allow to select the triplet randomly if it's set to `True`. Otherwise, it will take the first ones.
- `**krags` this parameter is not used. It only allow to quicly adapt a code that contain call to this function on upper classes without having to edit all the parameters.

**Returns**:

- `ndarray` A Numpy vector containing the input and the output (4 or 8 last elements of the vector).
- `int` The number of elements in the array that compose the output vector.
