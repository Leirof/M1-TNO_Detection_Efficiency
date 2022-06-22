# `class CCD`

`classes.ccd.CCD(id = None, data:ndarray = None, shot:Shot = None, triplet:Triplet = None, block:Block = None, dataPath:str = None)`

## Class attributes

- `all`: dictionnary containing CCD uid as key and the instance of the CCD as values.

---

## Class methods

No methods in this class

---

## Object attributes

- `uid : str`: unique identifier composed by the CCD id and the id of the parent Shot (ex: `1616681p15`).
- `id : int`: unique name of the block (ex: `15`).
- `data : ndarray`: the image of the CCD.
- `shot : Shot`: the instance of Shot object this CCD is included in.
- `triplet : Triplet`: the instance of Triplet object this CCD is included in.
- `block : Block`: the instance of Block object this CCD is included in.
- `dataPath : str`: path to the file that contain all the CCD data.
- `sky_background : ndarray`: the background of the sky contained in the CCD (image where extremums like stars were removed).
- `background_median : float`: the median of `sky_background`.
- `background_average : float`: the average of `sky_background`.
- `background_std : float`: the standard deviation of `sky_background`.
- `background_proportion : float`: the proportion of pixels that was kept when computating the `sky_background`.

---

## Object methods

### `unload()`

Delete the content of `data` and `sky_background` to free the RAM.

**inputs**: None

**Returns**: None

### `to_dict()`

Return a dictionary containing all the object informations. Useful to save it in a JSON format.

**inputs**: None

**Returns**:

- `dict`: The containing all the object informations except `data` and `sky_background`

### `to_ai_ready(**kwargs)`

Return a vector that can be used to train the AI.

**inputs**:

- `**krags` this parameter is not used. It only allow to quicly adapt a code that contain call to this function on upper classes without having to edit all the parameters.

**Returns**:

- `ndarray`: A Numpy vector containing the input and the output (4 or 8 last elements of the vector)
