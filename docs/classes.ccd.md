# `class CCD`

`classes.ccd.CCD(id = None, data:ndarray = None, shot:Shot = None, triplet:Triplet = None, block:Block = None, dataPath:str = None)`

A CCD is a part of a survey image. It contain most of the data acquired during the survey (ie. images).

**Parameters**

See object attributes below.

## Class attributes

### `all : dict`
Dictionnary containing CCD uid as key and the instance of the CCD as values.

---

## Class methods

No methods in this class

---

## Object attributes

### `uid : str`
Unique identifier composed by the CCD id and the id of the parent Shot (ex: `1616681p15`).
### `id : int`
Unique name of the block (ex: `15`).
### `data : ndarray`
The image of the CCD.
### `shot : Shot`
The instance of Shot object this CCD is included in.
### `triplet : Triplet`
The instance of Triplet object this CCD is included in.
### `block : Block`
The instance of Block object this CCD is included in.
### `dataPath : str`
Path to the file that contain all the CCD data.
### `sky_background : ndarray`
The background of the sky contained in the CCD (image where extremums like stars were removed).
### `background_median : float`
The median of `sky_background`.
### `background_average : float`
The average of `sky_background`.
### `background_std : float`
The standard deviation of `sky_background`.
### `background_proportion : float`
The proportion of pixels that was kept when computating the `sky_background`.

---

## Object methods

### unload

`unload()`

Delete the content of `data` and `sky_background` to free the RAM.

**Parameters**: None

**Returns**: None

### to_disct

`to_dict()`

Return a dictionary containing all the object information. Useful to save it in a JSON format.

**Parameters**: None

**Returns**:

- `dict`: The containing all the object information except `data` and `sky_background`

### to_ai_ready

`to_ai_ready(**kwargs)`

Return a vector that can be used to train the AI.

**Parameters**:

- `**krags` this parameter is not used. It only allow to quicly adapt a code that contain call to this function on upper classes without having to edit all the parameters.

**Returns**:

- `ndarray`: A Numpy vector containing the information about the CCD
