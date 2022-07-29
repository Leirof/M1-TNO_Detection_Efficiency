# class Shot

`classes.shot.Shot(id, ccdList=None, triplet=None, block=None, dataPath=None)`

A shot is basically an observation of the sky a a given time. This shot is usually decomposed in several CCD because of some technical constraints.

**Parameters**

See object attributes below.

## Class attributes

### `all : dict`
Dictionnary containing shot id as key and the instance of the shotss as values.

---

## Class methods

No methods in this class

---

## Object attributes

### `id : str`
Unique name of the shot (ex: `1625346`).
### `ccdList : list[CCD] | None`
List of `CCD` objects contained in this shot.
### `triplet : Triplet | None`
Parent triplet of this shot.
### `block : Block | None`
Parent block of this shot.
### `dataPath : str | None`
Path to the shot data.

---

## Object methods

### unload

`unload()`

Unload all the CCD of the shot to clear memory.

**Parameters**: None

**Returns**: None

### to_dict

`to_dict()`

Return a dictionary containing all the object information. Useful to save it in a JSON format.

**Parameters**: None

**Returns**:

- `dict`: The containing all the object information.

### to_ai_ready

`to_ai_ready(maxCCD=36, randomCCD=True, **kwargs)`

Return a vector that can be used to train the AI.

**Parameters**:

- `maxCCD : int`the minimum number of CCD included in the considered triplets. The default value correspond to the need of the original data set of used in this project. Be careful: if a considered triplet contain less CCD than this number, the output vectors will don't have the same dimension, which will lead to errors.
- `randomCCD : bool` if all triplets doesn't have the same amount of CCD, this parameter allow to select the triplet randomly if it's set to `True`. Otherwise, it will take the first ones.
- `**krags` this parameter is not used. It only allow to quicly adapt a code that contain call to this function on upper classes without having to edit all the parameters.

**Returns**:

- `ndarray`: A Numpy vector containing the informations about the shot.
